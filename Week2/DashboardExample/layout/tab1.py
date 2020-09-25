import dash_table
import dash_html_components as html
from mydatabase import transform
from app import app
from dash.dependencies import Output, Input
from layout import tab1, tab2, tab3

df = transform.get_data()

PAGE_SIZE = 50
layout = html.Div(dash_table.DataTable(
    id='table-sorting-filtering',
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in df.columns
    ],
    style_table={'overflowX': 'scroll'},
    style_cell={'height': '90', 'minWidth': '140px', 'width': '140px', 'maxWidth': '140px', 'whiteSpace': 'normal'},
    page_current=0,
    page_size=50,
    page_action='custom',
    filter_action='custom',
    filter_query='',
    sort_action='custom',
    sort_mode='multi',
    sort_by=[]
)
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(Output('table-sorting-filtering', 'data'),
              [Input('table-sorting-filtering', "page_current"),
               Input('table-sorting-filtering', "page_size"),
               Input('table-sorting-filtering', 'sort_by'),
               Input('table-sorting-filtering', 'filter_query'),
               Input('rating-95', 'value'),
               Input('price-slider', 'value'),
               Input('country-drop', 'value'),
               Input('province-drop', 'value'),
               Input('variety-drop', 'value')
               ])
def update_table(page_current, page_size, sort_by, filter, ratingcheck, prices, country, province, variety):
    filtering_expressions = filter.split(' && ')
    dff = df

    low = prices[0]
    high = prices[1]

    dff = dff.loc[(dff['price'] >= low) & (dff['price'] <= high)]
    if ratingcheck == ['Y']:
        dff = dff.loc[dff['rating'] >= 95]
    else:
        dff

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values([col['column_id'] for col in sort_by], ascending=[
            col['direction'] == 'asc'
            for col in sort_by
        ],
                              inplace=False
                              )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')