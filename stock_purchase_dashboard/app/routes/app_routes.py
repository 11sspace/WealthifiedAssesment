from flask_restx import Namespace, fields

purchase_route = Namespace("purchase_summary", description="Investor-wise Purchase Summary per Mutual Fund")

investor_model = purchase_route.model("InvestorModel", {
    "investor_name": fields.String,
    "total_purchase_amount": fields.Float,
    "total_units": fields.Float,
})

mutual_fund_model = purchase_route.model("MutualFundModel", {
    "mutual_fund_name": fields.String,
    "investor_summary": fields.List(fields.Nested(investor_model))
})
mutual_fund_model_response=purchase_route.model("MutualFundModelResponse",{
    "data":fields.List(fields.Nested(mutual_fund_model))
})

###########################################################################


fund_summary_model = purchase_route.model("FundSummaryModel", {
    "mutual_fund_name": fields.String,
    "total_purchase_amount": fields.Float,
    "total_units": fields.Float
})
investor_summary_model_response = purchase_route.model("InvestorSummaryModelResponse", {
    "investor_name": fields.String,
    "mutual_fund_summary": fields.List(fields.Nested(fund_summary_model))
})
investor_summary_listing_response=purchase_route.model('InvestorSummaryListingResponse',{
    "data":fields.List(fields.Nested(investor_summary_model_response))
})

##########################################################################################


investor_summary = purchase_route.model("InvestorSummary", {
    "pan": fields.String,
    "investor_name":fields.String,
    "total_invested_amount": fields.Float
})
investor_summary_reponse=purchase_route.model('InvestorSummaryReponse',{
    "data":fields.List(fields.Nested(investor_summary))
})

#####################################################################################

avg_nav_model = purchase_route.model("AvgNavModel", {
    "scheme": fields.String,
    "total_amount": fields.Float,
    "total_units": fields.Float,
    "average_nav": fields.Float,
})
mutual_fund_summary_response = purchase_route.model("MutualFundSummaryResponse", {
    "total_amount_invested": fields.Float,
    "total_units_purchased": fields.Float,
    "average_nav_per_fund": fields.List(fields.Nested(avg_nav_model))
})

