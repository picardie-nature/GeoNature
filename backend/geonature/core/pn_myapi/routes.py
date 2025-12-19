from flask import Blueprint, request
from sqlalchemy.sql import text, bindparam

from geonature.utils.env import DB
from utils_flask_sqla.response import json_resp

routes = Blueprint("myapi", __name__)


@routes.route("/calendar_heatmap", methods=["GET"])
@json_resp
def calendar_heatmap():
    params = request.args
    if "cd_nom" not in params:
        return []
    
    query = """
         SELECT
         EXTRACT(DOY FROM date_min) AS "doy",
             count(*) AS nb_obs
         FROM pn_work_synthese.pn_work_synthese_usable s
         JOIN taxonomie.taxref tx USING (cd_nom)
         JOIN taxonomie.pn_custom_taxref_tree_parents ttp ON ttp.cd_nom = tx.cd_ref
         WHERE ttp.cd_nom_parent =:cd_nom
             AND date_max::date = date_min::date
             AND date_min >= now()-'10 years'::interval
         GROUP BY EXTRACT(DOY FROM date_min)
     """

    t = text(query)
    result = DB.engine.execute(t, cd_nom=params["cd_nom"])
    return [{"doy": res.doy, "nb_obs": res.nb_obs} for res in result]
