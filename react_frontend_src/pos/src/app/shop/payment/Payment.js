import React, { Component } from "react"
import { intlShape } from "react-intl"
import PropTypes from "prop-types"
import { v4 } from "uuid"

import PageTemplate from "../../../components/PageTemplate"

class Payment extends Component {
    constructor(props) {
        super(props)
        console.log(props)
    }

    PropTypes = {
        intl: intlShape.isRequired,
        setPageTitle: PropTypes.function,
        app: PropTypes.object,
    }

    componentWillMount() {
        this.props.setPageTitle(
            this.props.intl.formatMessage({ id: 'app.pos.shop.payment.page_title' })
        )
    }
    
    render() {

        return (
            <PageTemplate app_state={this.props.app}>

                Payment screen will go here
            </PageTemplate>
        )
    }
}

export default Payment
