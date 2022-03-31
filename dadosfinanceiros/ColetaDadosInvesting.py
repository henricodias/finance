import investpy as inv

#inv.get_stocks_overview(country="Brazil", as_json= False, n_results= 1000)

ativo = "PETR4"

#inv.get_stock_company_profile(ativo, country="Brazil")

#inv.get_stock_financial_summary(ativo,
#                                country= "Brazil",
#                                summary_type= "income_statement",
#                                period= "quaterly")
#inv.get_bond_information(ativo,
#                         country= "Brazil",
#                         as_json= False).transpose()
petr = inv.search_quotes(text= "petrobras",
                         products= ["stocks"],
                         countries= ["Brazil"],
                         n_results= 1)

print(petr)