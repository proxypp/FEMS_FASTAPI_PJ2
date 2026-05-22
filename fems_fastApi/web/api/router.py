from fastapi.routing import APIRouter
from fems_fastApi.web.api import auth, base_code, base_file, conf_menu, emission_factor, emission_factor_usage, energy_amount_trend, energy_source, energy_usage_pred, equip, equip_compare, equip_insp_compare, equip_interface, equip_plan_mmdd, equip_plan_yymm, equip_result_search, item, meter, meter_energy_search, month_prod_emission, period_energy_usage, prev_year_month_compare, prod_order, prod_result, real_time_usage, tariff, user, utility_amount, utility_manual, utility_source_usage, utility_usage_month

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(base_code.router, prefix="/base-code", tags=["Base Code"])
api_router.include_router(base_file.router, prefix="/base-file", tags=["Base File"])
api_router.include_router(equip.router, prefix="/equip", tags=["Equip"])
api_router.include_router(item.router, prefix="/item", tags=["Item"])
api_router.include_router(
    utility_usage_month.router,
    prefix="/utility-usage-month",
    tags=["Utility Usage Month"],
)
api_router.include_router(
    energy_source.router,
    prefix="/energy-source",
    tags=["Energy Source"],
)
api_router.include_router(meter.router, prefix="/meter", tags=["Meter"])
api_router.include_router(tariff.router, prefix="/tariff", tags=["Tariff"])
api_router.include_router(emission_factor.router, prefix="/emission-factor", tags=["Emission Factor"])
api_router.include_router(emission_factor_usage.router, prefix="/emission-factor-usage", tags=["Emission Factor Usage"])
api_router.include_router(
    month_prod_emission.router,
    prefix="/month-prod-emission",
    tags=["Month Prod Emission"],
)
api_router.include_router(prod_order.router, prefix="/prod-order", tags=["Prod Order"])
api_router.include_router(prod_result.router, prefix="/prod-result", tags=["Prod Result"])
api_router.include_router(utility_manual.router, prefix="/utility-manual", tags=["Utility Manual"])
api_router.include_router(utility_amount.router, prefix="/utility-amount", tags=["Utility Amount"])
api_router.include_router(
    utility_source_usage.router,
    prefix="/utility-source-usage",
    tags=["Utility Source Usage"],
)
api_router.include_router(
    real_time_usage.router,
    prefix="/real-time-usage",
    tags=["Real Time Usage"],
)
api_router.include_router(
    period_energy_usage.router,
    prefix="/period-energy-usage",
    tags=["Period Energy Usage"],
)
api_router.include_router(
    energy_amount_trend.router,
    prefix="/energy-amount-trend",
    tags=["Energy Amount Trend"],
)
api_router.include_router(
    prev_year_month_compare.router,
    prefix="/prev-year-month-compare",
    tags=["Prev Year Month Compare"],
)
api_router.include_router(
    equip_compare.router,
    prefix="/equip-compare",
    tags=["Equip Compare"],
)
api_router.include_router(
    equip_plan_yymm.router,
    prefix="/equip-plan-yymm",
    tags=["Equip Plan Yymm"],
)
api_router.include_router(
    equip_plan_mmdd.router,
    prefix="/equip-plan-mmdd",
    tags=["Equip Plan Mmdd"],
)
api_router.include_router(
    equip_insp_compare.router,
    prefix="/equip-insp-compare",
    tags=["Equip Insp Compare"],
)
api_router.include_router(
    equip_result_search.router,
    prefix="/equip-result-search",
    tags=["Equip Result Search"],
)
api_router.include_router(
    meter_energy_search.router,
    prefix="/meter-energy-search",
    tags=["Meter Energy Search"],
)
api_router.include_router(
    conf_menu.router,
    prefix="/conf-menu",
    tags=["Conf Menu"],
)
api_router.include_router(
    equip_interface.router,
    prefix="/equip-interface",
    tags=["Equip Interface"],
)
api_router.include_router(
    energy_usage_pred.router,
    prefix="/energy-usage-pred",
    tags=["Energy Usage Pred"],
)
