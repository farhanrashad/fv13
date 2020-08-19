# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Product Exchange",
  "summary"              :  "This module is use to exchange products of previous order in running point of sale session.",
  "category"             :  "Point Of Sale",
  "version"             : '0.1',
  "author"               :  "Webkul Software Pvt. Ltd",
  "depends"              :  ['pos_order_return'],
  "data"                 :  [
                             'views/template.xml',
                            ],
  "qweb"                 :  ['static/src/xml/pos_product_exchange.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}