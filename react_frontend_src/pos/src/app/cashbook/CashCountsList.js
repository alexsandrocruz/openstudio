import React, { Component } from "react"
import { intlShape } from "react-intl"
import PropTypes from "prop-types"
import { v4 } from "uuid"
import { NavLink } from 'react-router-dom'

import PageTemplate from "../../components/PageTemplate"
import Currency from "../../components/ui/Currency"


class CashCountList extends Component {
    constructor(props) {
        super(props)
        console.log("Balance list props:")
        console.log(props)
    }

    PropTypes = {
        intl: intlShape.isRequired,
        app: PropTypes.object,
        balance: PropTypes.object,
    }

    componentWillMount() {
    }

    render() {
        const render_items = []
        const loading = this.props.cashbook.cash_counts_loading
        const loaded = this.props.cashbook.cash_counts_loaded


        return (
            <div className="box box-solid expenses-list"> 
                <div className="box-header">
                    <h3 className="box-title">
                        <i className="fa fa-money"></i> Cash count
                    </h3>
                </div>
                <div className="box-body">
                    {(!loaded) ? "Loading counts..." :
                        <div>
                            <div>
                                <span className="bold">Opening: </span> 
                                <Currency amount={this.props.cashbook.cash_counts_data.opening.Amount} />
                            </div>
                            <div>
                                <span className="bold">Closing: </span> 
                                <Currency amount={this.props.cashbook.cash_counts_data.closing.Amount} />
                            </div>
                        </div>
                    }
                </div>
            </div>
        )
    }
}

export default CashCountList
