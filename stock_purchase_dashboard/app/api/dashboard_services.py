import datetime

from flask import request
from flask_restx import Resource, abort
from sqlalchemy import text, func, Numeric, cast

from .helper import date_check
from ..db_model.models import MutualFundTransaction
from ..routes.app_routes import purchase_route, mutual_fund_model_response, investor_summary_listing_response, \
    investor_summary_reponse, mutual_fund_summary_response
from .. import db
date_filters={
        "start_date": {"description": "Start date in YYYY-MM-DD format", "type": "string"},
        "end_date": {"description": "End date in YYYY-MM-DD format", "type": "string"}
    }
@purchase_route.route('/')
class InvestorSummary(Resource):
    @purchase_route.marshal_with(mutual_fund_model_response)
    @purchase_route.doc(params=date_filters)
    def get(self):
        """
        Investor-wise Purchase Summary per Mutual Fund
        :return:
        """
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date") if request.args.get("end_date") else request.args.get("start_date")
        if start_date_str:
            start_date_str,end_date_str=date_check(start_date_str,end_date_str)
        sql_condition=''
        if start_date_str:
            sql_condition=' and trad_date::date BETWEEN :start_date AND :end_date '
        sql = text(f"""
        with cte as (
                    select scheme as mutual_fund_name,inv_name,SUM(amount) as total_purchase_amount,
                    SUM(units) as total_units
                    from mutual_fund_transactions
                    where deleted = false {sql_condition}
                       
                       group by  scheme,inv_name
                    )
                    
                    select mutual_fund_name,
                    jsonb_agg(json_build_object(
                                                    'investor_name', inv_name,
                                'total_purchase_amount', total_purchase_amount,
                                'total_units', total_units
                    )) investor_summary
                    from cte
                    group by mutual_fund_name
                """)
        result = db.engine.execute(sql,start_date= start_date_str,
                                    end_date= end_date_str
                                    )

        response = []
        for row in result:
            response.append({
                "mutual_fund_name": row["mutual_fund_name"],
                "investor_summary": row["investor_summary"]
            })

        return {"data":response}
@purchase_route.route('/investor_summary')
class MutualFundInvestorSummary(Resource):
    @purchase_route.marshal_with(investor_summary_listing_response)
    @purchase_route.doc(params=date_filters)
    def get(self):
        """
        Mutual Fund-wise Summary per Investor
        :return:
        """
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date") or start_date_str

        if start_date_str:
            start_date_str, end_date_str = date_check(start_date_str, end_date_str)

        sql_condition = ''
        if start_date_str:
            sql_condition = ' AND trad_date::date BETWEEN :start_date AND :end_date '

        sql = text(f"""
            WITH investor_cte AS (
                SELECT 
                    inv_name AS investor_name,
                    scheme AS mutual_fund_name,
                    SUM(amount) AS total_purchase_amount,
                    SUM(units) AS total_units
                FROM mutual_fund_transactions
                WHERE deleted = false {sql_condition}
                GROUP BY inv_name, scheme
            )
            SELECT investor_name,
                   jsonb_agg(json_build_object(
                       'mutual_fund_name', mutual_fund_name,
                       'total_purchase_amount', total_purchase_amount,
                       'total_units', total_units
                   )) AS mutual_fund_summary
            FROM investor_cte
            GROUP BY investor_name
        """)

        result = db.engine.execute(sql, start_date=start_date_str, end_date=end_date_str)

        response = []
        for row in result:
            response.append({
                "investor_name": row["investor_name"],
                "mutual_fund_summary": row["mutual_fund_summary"]
            })

        return {"data": response}


@purchase_route.route("/investor-purchase-summary")
class InvestorPurchaseSummary(Resource):
    @purchase_route.doc(params={
        'start_date': 'Start date in YYYY-MM-DD',
        'end_date': 'End date in YYYY-MM-DD',
    })
    @purchase_route.marshal_list_with(investor_summary_reponse)
    def get(self):
        """
        Investor List with Purchase Details
        :return
        """
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if start_date:
            start_date, end_date = date_check(start_date, end_date)
        # if not start_date or not end_date:
        #     abort(400, "start_date and end_date query parameters are required")

        # try:
        #     start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        #     end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        # except ValueError:
        #     abort(400, "Dates must be in YYYY-MM-DD format")
        filters = [MutualFundTransaction.deleted == False]
        if start_date is not None:
            filters.append(MutualFundTransaction.trad_date >= start_date)
        if end_date is not None:
            filters.append(MutualFundTransaction.trad_date <= end_date)
        results = db.session.query(
            MutualFundTransaction.pan.label("pan"),
            MutualFundTransaction.inv_name.label("investor_name"),
            func.sum(MutualFundTransaction.amount).label("total_invested_amount")
        ).filter(
            *filters
        ).group_by(
            MutualFundTransaction.pan,
            MutualFundTransaction.inv_name
        ).all()

        return {"data": results}
@purchase_route.route('/mutual_fund/summary')
class MutualFundSummary(Resource):
    @purchase_route.marshal_with(mutual_fund_summary_response)
    def get(self):
        """Mutual Fund Summary
        :return"""
        # Total amount invested & total units
        overall_totals = db.session.query(
            func.sum(MutualFundTransaction.amount).label("total_amount_invested"),
            func.sum(MutualFundTransaction.units).label("total_units_purchased")
        ).filter(
            MutualFundTransaction.deleted.is_(False)
        ).first()

        # Average NAV per mutual fund (grouped by scheme or prodcode)
        average_navs = db.session.query(
            MutualFundTransaction.scheme.label("scheme"),
            func.round(cast(func.sum(MutualFundTransaction.amount), Numeric), 2).label("total_amount"),
            func.round(cast(func.sum(MutualFundTransaction.units), Numeric), 2).label("total_units"),
            func.round(
                cast(func.sum(MutualFundTransaction.amount), Numeric) /
                func.nullif(cast(func.sum(MutualFundTransaction.units), Numeric), 0), 2
            ).label("average_nav")
        ).filter(
            MutualFundTransaction.deleted.is_(False)
        ).group_by(
            MutualFundTransaction.scheme
        ).all()

        return {
            "total_amount_invested": round(overall_totals.total_amount_invested,2) or 0,
            "total_units_purchased": round(overall_totals.total_units_purchased,2) or 0,
            "average_nav_per_fund": average_navs
        }

