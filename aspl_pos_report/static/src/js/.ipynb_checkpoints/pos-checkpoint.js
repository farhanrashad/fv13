odoo.define('aspl_pos_report.pos', function (require) {
"use strict";

    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;

    var add_productsummary_button = screens.ActionButtonWidget.extend({
        template: 'AddProductSummaryButton',
        button_click: function(){
            this.gui.show_popup('product_summary_report_wizard');
        },
    });
    screens.define_action_button({
        'name': 'productsummarybutton',
        'widget': add_productsummary_button,
        'condition': function(){
            return this.pos.config.print_product_summary;
        },
    });

    var PosOrderSummary = screens.ActionButtonWidget.extend({
		template : 'PosOrderSummary',
		button_click : function() {
			this.gui.show_popup('order_summary_popup');
		},
	});
	screens.define_action_button({
		'name' : 'ordersummary',
		'widget' : PosOrderSummary,
		'condition' : function() {
			return this.pos.config.enable_order_summary;
		},
	});

	var add_paymentsummary_button = screens.ActionButtonWidget.extend({
        template: 'AddPaymentSummaryButton',
        button_click: function(){
            this.gui.show_popup('payment_summary_report_wizard');
        },
    });
    screens.define_action_button({
        'name': 'salesummarybutton',
        'widget': add_paymentsummary_button,
        'condition': function(){
            return this.pos.config.payment_summary;
        },
    });

    var product_summary_popup = PopupWidget.extend({
	    template: 'ProductSummaryReportPopupWizard',
	    show: function(options){
	        options = options || {};
	        this._super(options);
	        var self = this;
	        self.pos.signature = false;
	    	$('input#start_date').focus();
	    	var no_of_report = this.pos.config.no_of_copy_receipt;
	    	$('input#no_of_summary').val(no_of_report);
	    	var today_date = new Date().toISOString().split('T')[0];
            var date = new Date();
            var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
            var first_date_of_month = firstDay.toISOString().split('T')[0];
            if(this.pos.config.current_month_date){
                $('input#start_date').val(first_date_of_month);
                $('input#end_date').val(today_date);
            }
            $("#start_date").change(function() {
                if($("#start_date").val() != ""){
                     $('#start_date').css('border','');
                }
            });
            $("#end_date").change(function() {
                if($("#end_date").val() != ""){
                    $('#end_date').css('border','');
                }
            });
            if(no_of_report <= 0){
	    	    $('input#no_of_summary').val(1);
	    	} else{
	    	    $('input#no_of_summary').val(no_of_report);
	    	}
            $("#no_of_summary").change(function() {
                if($("#no_of_summary").val() != ""){
                    $('#no_of_summary').css('border','');
                }
            });
            if(this.pos.config.signature){
                self.pos.signature = true;
            }
	    },
	    click_confirm: function(){
	        var self = this;
	        var from_date = $('input#start_date').val();
	        var to_date = $('input#end_date').val();
	        var no_of_copies = $('input#no_of_summary').val();
	        var order = this.pos.get_order();
	        var today_date = new Date().toISOString().split('T')[0];
            var report_value = [];
	        order.set_order_summary_report_mode(true);
            self.pos.from_date = from_date;
            self.pos.to_date = to_date;
            if(no_of_copies <= 0){
                 $('#no_of_summary').css('border','1px solid red');
                 return;
            }
            $("input:checked").each(function () {
   	            var id = $(this).attr("id");
   	            report_value.push(id);
   	        });
            if(from_date == "" && to_date == "" || from_date != "" && to_date == "" || from_date == "" && to_date != "" ){
                if(from_date == ""){
                    $('#start_date').css('border','1px solid red');
                }
                if(to_date == ""){
                    $('#end_date').css('border','1px solid red');
                }
                return;
            } else if(from_date > to_date){
                alert("Start date should not be greater than end date");
            } else{
	            var val = {
	                'start_date':start_date.value,
	                'end_date':end_date.value,
	                'summary': report_value
	            }
	            var params = {
	                model: 'pos.order',
	                method: 'product_summary_report',
	                args: [val],
	            }
	            rpc.query(params, {async: false}).then(function(res){
	                if(res){
	                    if(Object.keys(res['category_summary']).length == 0 && Object.keys(res['product_summary']).length == 0 &&
	                        Object.keys(res['location_summary']).length == 0 && Object.keys(res['payment_summary']).length == 0){
	                        order.set_order_summary_report_mode(false);
	                        alert("No records found!");
	                    } else{
	                        self.pos.product_total_qty = 0.0;
	                        self.pos.category_total_qty = 0.0;
	                        self.pos.payment_summary_total = 0.0;
	                        if(res['product_summary']){
	                            _.each(res['product_summary'], function(value,key){
	                                    self.pos.product_total_qty += value;
	                                });
	                        }
	                        if(res['category_summary']){
	                            _.each(res['category_summary'], function(value,key) {
	                                    self.pos.category_total_qty += value;
	                                });
	                        }
	                        if(res['payment_summary']){
	                            _.each(res['payment_summary'], function(value,key) {
	                                    self.pos.payment_summary_total += value;
	                                });
	                        }
	                    order.set_product_summary_report(res);
	                    var product_summary_key = Object.keys(order.get_product_summary_report()['product_summary']);
	                    if(product_summary_key.length == 0){
	                        var product_summary_data = false;
	                    } else {
	                        var product_summary_data = order.get_product_summary_report()['product_summary'];
	                    }
	                    var category_summary_key = Object.keys(order.get_product_summary_report()['category_summary']);
	                    if(category_summary_key.length == 0){
	                        var category_summary_data = false;
	                    } else {
	                        var category_summary_data = order.get_product_summary_report()['category_summary'];
	                    }
	                    var payment_summary_key = Object.keys(order.get_product_summary_report()['payment_summary']);
	                    if(payment_summary_key.length == 0){
	                    var payment_summary_data = false;
	                    } else {
	                        var payment_summary_data = order.get_product_summary_report()['payment_summary'];
	                    }
	                    var location_summary_key = Object.keys(order.get_product_summary_report()['location_summary']);
	                    if(location_summary_key.length == 0){
	                        var location_summary_data = false;
	                    } else {
	                        var location_summary_data = order.get_product_summary_report()['location_summary'];
	                    }
	                    if (self.pos.config.iface_print_via_proxy) {
	                        var receipt = "";
	                        for (var step = 0; step < no_of_copies; step++) {
	                            receipt = QWeb.render('ProductSummaryReportXmlReceipt', {
	                                widget: self,
	                                pos: self.pos,
	                                order: order,
	                                receipt: order.export_for_printing(),
	                                product_details: product_summary_data,
	                                category_details:category_summary_data,
	                                payment_details: payment_summary_data,
	                                location_details:location_summary_data,
	                            });
	                            self.pos.proxy.print_receipt(receipt);
	                        }
	                    } else{
	                        self.gui.show_screen('receipt');
	                        }
	                    }
	                }
	            });
            }
	    },
	});
    gui.define_popup({name:'product_summary_report_wizard', widget: product_summary_popup});

    var OrderSummaryPopupWidget = PopupWidget.extend({
	    template: 'OrderSummaryPopupWidget',
	    show: function(options){
	        options = options || {};
	        this._super(options);
	        $('input#order_start_date').focus();
	        var self = this;
	        var today_date = new Date().toISOString().split('T')[0];
	        self.pos.signature = false;
	        if (self.pos.config.signature){
	        	self.pos.signature = true;
	        }
	        var date = new Date();
	        var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
	        var first_date = firstDay.toISOString().split('T')[0];
	    	var no_of_report = this.pos.config.no_of_copy_receipt;
	    	if(no_of_report <= 0){
	    		$('input#no_of_copies').val(1);
	    	}else{
	    		$('input#no_of_copies').val(no_of_report);
	    	}
	        if(this.pos.config.current_month_date){
	    		$('input#order_start_date').val(first_date);
	    		$('input#order_end_date').val(today_date);
	    	}
	    	$("#order_start_date").change(function() {
                if($("#order_start_date").val()){
                     $('#order_start_date').css('border','');
                }
            });
            $("#order_end_date").change(function() {
                if($("#order_end_date").val()){
                    $('#order_end_date').css('border','');
                }
            });
	    },
	    click_confirm: function(){
	    	var self = this;
	    	var value = {};
	    	var order = this.pos.get_order();
	    	self.pos.no = $('input#no_of_copies').val();
	    	self.pos.from_date = $('input#order_start_date').val();
	    	self.pos.to_date = $('input#order_end_date').val();
	    	var today_date = new Date().toISOString().split('T')[0];
	    	var state = states.value;
	    	var custom_receipt = true;
	    	var report_list = [];
	    	var client = this.pos.get_client();
	    	order.set_receipt(custom_receipt);
	    	$("input:checked").each(function () {
    	        var id = $(this).attr("id");
    	        report_list.push(id);
    	    });
	    	if($('input#no_of_copies').val() <= 0){
	    		$('input#no_of_copies').css('border','1px solid red');
	    		return;
	    	}
    	   	if(self.pos.from_date == "" && self.pos.to_date == "" || self.pos.from_date != "" && self.pos.to_date == "" || self.pos.from_date == "" && self.pos.to_date != "" ){
    	   		if(self.pos.from_date == ""){
    	   			$('#order_start_date').css('border','1px solid red');
    	   		}
    	   		if(self.pos.to_date == ""){
    	   			$('#order_end_date').css('border','1px solid red');
    	   		}
    	   		return;
	   		} else if(self.pos.from_date > self.pos.to_date) {
	   			alert("End date must be greater");
	   			return;
	   		} else{
	   			value = {
   	    			'start_date' : self.pos.from_date,
   	    			'end_date' : self.pos.to_date,
   	    			'state' : state,
   	    			'summary' :report_list
   		    	}
   		    	var params = {
	    			model : 'pos.order',
	    			method : 'order_summary_report',
	    			args : [value],
   		    	}
   		    	rpc.query(params,{async:false}).then(function(res){
   		    		self.pos.state = false;
   		    		if(res['state']){
   		    			self.pos.state = true
   		    		}
   		    		if(res){
   		    			if(Object.keys(res['category_report']).length == 0 && Object.keys(res['order_report']).length == 0 &&
   		    					Object.keys(res['payment_report']).length == 0){
   		    					order.set_receipt(false);
   		    					alert("No records found!");
   		    			} else{
   			    			self.pos.total_categ_amount = 0.00;
   			    			self.pos.total_amount = 0.00;
   			    			if(res['category_report']){
   			    				if(self.pos.state){
   			    					_.each(res['category_report'], function(value,key) {
   				                        self.pos.total_categ_amount += value[1];
			                        });
   			    				}
   			    			}
   			    			if(res['payment_report']){
   			    				if(self.pos.state){
	   			    				_.each(res['payment_report'], function(value,key) {
		   		                        self.pos.total_amount += value;
		   		                    });
   			    				}
   			    			}
   			    			order.set_order_list(res);
   			    			if(order.get_receipt()) {
   			   		        	var category_data = '';
   			   		        	var order_data = '';
   			   		        	var payment_data = '';
   			   		        	if(Object.keys(order.get_order_list().order_report).length == 0 ){
   			   		        		order_data = false;
   			   		        	}else{
   			   		        		order_data = order.get_order_list()['order_report']
   			   		        	}
   			   		        	if(Object.keys(order.get_order_list().category_report).length == 0 ){
   			   		        		category_data = false;
   			   		        	}else{
   			   		        		category_data = order.get_order_list()['category_report']
   			   		        	}
   			   		        	if(Object.keys(order.get_order_list().payment_report).length == 0 ){
   			   		        		payment_data = false;
   			   		        	}else{
   			   		        		payment_data = order.get_order_list()['payment_report']
   			   		        	}
   				   		    	var receipt = '';
   				   		    	if(self.pos.config.iface_print_via_proxy){
   				   		    		for (var i=0;i < self.pos.no;i++) {
   				   		    			receipt = QWeb.render('OrderXmlReceipt', {
   						    				widget: self,
   						    				pos: self.pos,
   						    				order: order,
   						    				receipt: order.export_for_printing(),
   						    				order_report : order_data,
   						    				category_report : category_data,
   						    				payment_report : payment_data,
   						    			});
   				   		    		}
   					   		    	self.pos.proxy.print_receipt(receipt);
   				   		    	} else{
   				   		    		self.gui.show_screen('receipt')
   				   		    	}
   			   		        }
   		    			}
   		    		}
   		    	});
	   		}
	    },
	});
	gui.define_popup({name:'order_summary_popup',widget: OrderSummaryPopupWidget});

    var sales_summary_popup = PopupWidget.extend({
	    template: 'PaymentSummaryReportPopupWizard',
	    show: function(options){
	        options = options || {};
	        this._super(options);
	        var self = this;
	    	var today_date = new Date().toISOString().split('T')[0];
            var date = new Date();
            var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
            var first_date_of_month = firstDay.toISOString().split('T')[0];
            if(this.pos.config.current_month_date){
                $('input#pay_start_date').val(first_date_of_month);
                $('input#pay_end_date').val(today_date);
            }
            $("#pay_start_date").change(function() {
                if($("#pay_start_date").val()){
                     $('#pay_start_date').css('border','');
                }
            });
            $("#pay_end_date").change(function() {
                if($("#pay_end_date").val()){
                    $('#pay_end_date').css('border','');
                }
            });
            $('input#pay_start_date').focus();
	    },
	    click_confirm: function(){
	        var self = this;
	        var order = this.pos.get_order();
	        var from_date = $('input#pay_start_date').val();
	        var to_date = $('input#pay_end_date').val();
	        var today_date = new Date().toISOString().split('T')[0];
	        var data = dropdown_data.value;
	        order.set_sales_summary_mode(true);
	        var pop_start_date = from_date.split('-');
            self.pos.from_date  = pop_start_date[2] + '-' + pop_start_date[1] + '-' + pop_start_date[0];
            var pop_end_date = to_date.split('-');
            self.pos.to_date  = pop_end_date[2] + '-' + pop_end_date[1] + '-' + pop_end_date[0];
            if(from_date == "" && to_date == "" || from_date != "" && to_date == "" || from_date == "" && to_date != "" ){
                if(!from_date){
                    $('#pay_start_date').css('border','1px solid red');
                }
                if(!to_date){
                    $('#pay_end_date').css('border','1px solid red');
                }
                return;
            } else if(from_date > to_date){
                alert("Start date should not be greater than end date");
            } else{
                var val = {
                    'start_date':from_date,
                    'end_date':to_date,
                    'summary': data
                }
                var params = {
                    model: 'pos.order',
                    method: 'payment_summary_report',
                    args: [val],
                }
                rpc.query(params, {async: false}).then(function(res){
                    if(res){
                        if(Object.keys(res['journal_details']).length == 0 && Object.keys(res['salesmen_details']).length == 0){
                        order.set_sales_summary_mode(false);
                        alert("No records found!");
                        } else{
                            order.set_sales_summary_vals(res);
                            var journal_key = Object.keys(order.get_sales_summary_vals()['journal_details']);
                            if(journal_key.length > 0){
                                var journal_summary_data = order.get_sales_summary_vals()['journal_details'];
                            } else {
                                var journal_summary_data = false;
                            }
                            var sales_key = Object.keys(order.get_sales_summary_vals()['salesmen_details']);
                            if(sales_key.length > 0){
                                var sales_summary_data = order.get_sales_summary_vals()['salesmen_details'];
                            } else {
                                var sales_summary_data = false;
                            }
                            var total = Object.keys(order.get_sales_summary_vals()['summary_data']);
                            if(total.length > 0){
                                var total_summary_data = order.get_sales_summary_vals()['summary_data'];
                            } else {
                                var total_summary_data = false;
                            }
                            if (self.pos.config.iface_print_via_proxy) {
                                var receipt = "";
                                receipt = QWeb.render('PaymentSummaryReportXmlReceipt', {
                                    widget: self,
                                    pos: self.pos,
                                    order: order,
                                    receipt: order.export_for_printing(),
                                    journal_details: journal_summary_data,
                                    salesmen_details: sales_summary_data,
                                    total_summary : total_summary_data
                                });
                               self.pos.proxy.print_receipt(receipt);
                            } else{
                                self.gui.show_screen('receipt');
                           }
                        }
                    }
                });
            }
	    },
	});
    gui.define_popup({name:'payment_summary_report_wizard', widget: sales_summary_popup});

    var _super_order = models.Order.prototype;
     models.Order = models.Order.extend({
        set_order_summary_report_mode: function(order_summary_report_mode) {
            this.order_summary_report_mode = order_summary_report_mode;
        },
        get_order_summary_report_mode: function() {
            return this.order_summary_report_mode;
        },
        set_product_summary_report :function(product_summary_report) {
            this.product_summary_report = product_summary_report;
        },
        get_product_summary_report: function() {
            return this.product_summary_report;
        },
        set_sales_summary_mode: function(sales_summary_mode) {
            this.sales_summary_mode = sales_summary_mode;
        },
        get_sales_summary_mode: function() {
            return this.sales_summary_mode;
        },
        set_sales_summary_vals :function(sales_summary_vals) {
            this.sales_summary_vals = sales_summary_vals;
        },
        get_sales_summary_vals: function() {
            return this.sales_summary_vals;
        },
        set_receipt: function(custom_receipt) {
        	this.custom_receipt = custom_receipt;
        },
        get_receipt: function() {
        	return this.custom_receipt;
        },
        set_order_list: function(order_list) {
        	this.order_list = order_list;
        },
        get_order_list: function() {
        	return this.order_list;
        },
     });

     screens.ReceiptScreenWidget.include({
        render_receipt: function() {
        var no = $('#no_of_summary').val();
        var order_no = $('input#no_of_copies').val();
        var order = this.pos.get_order();
        if(order.get_order_summary_report_mode()){
            var product_summary_key = Object.keys(order.get_product_summary_report()['product_summary'] ? order.get_product_summary_report()['product_summary'] :false );
            if(product_summary_key.length > 0){
            	var product_summary_data = order.get_product_summary_report()['product_summary'];
            } else {
            	var product_summary_data = false;
            }
            var category_summary_key = Object.keys(order.get_product_summary_report()['category_summary']);
             if(category_summary_key.length > 0){
            	var category_summary_data = order.get_product_summary_report()['category_summary'];
            } else {
            	var category_summary_data = false;
            }
             var payment_summary_key = Object.keys(order.get_product_summary_report()['payment_summary']);
             if(payment_summary_key.length > 0){
            	 var payment_summary_data = order.get_product_summary_report()['payment_summary'];
            } else {
            	var payment_summary_data = false;
            }
            var location_summary_key = Object.keys(order.get_product_summary_report()['location_summary']);
             if(location_summary_key.length > 0){
            	 var location_summary_data = order.get_product_summary_report()['location_summary'];
            } else {
            	var location_summary_data = false;
            }
            var receipt = "";
            for (var step = 0; step < no; step++) {
                receipt += QWeb.render('ProductSummaryReport',{
                    widget:this,
                    order: order,
                    receipt: order.export_for_printing(),
                    product_details: product_summary_data,
                    category_details: category_summary_data,
                    payment_details: payment_summary_data,
                    location_details:location_summary_data,
                })
            }
            this.$('.pos-receipt-container').html(receipt);
        }else if(order.get_receipt()) {
            var category_data = '';
            var order_data = '';
            var payment_data = '';
            if(Object.keys(order.get_order_list().order_report).length == 0 ){
                order_data = false;
            }else{
                order_data = order.get_order_list()['order_report']
            }
            if(Object.keys(order.get_order_list().category_report).length == 0 ){
                category_data = false;
            }else{
                category_data = order.get_order_list()['category_report']
            }
            if(Object.keys(order.get_order_list().payment_report).length == 0 ){
                payment_data = false;
            }else{
                payment_data = order.get_order_list()['payment_report']
            }
            var receipt = "";
            for(var i=0;i < order_no;i++){
                receipt += QWeb.render('CustomTicket',{
                    widget:this,
                    order: order,
                    receipt: order.export_for_printing(),
                    order_report : order_data,
                    category_report : category_data,
                    payment_report : payment_data
                })
            }
            this.$('.pos-receipt-container').html(receipt);
        }else if(order.get_sales_summary_mode()) {
             var journal_key = Object.keys(order.get_sales_summary_vals()['journal_details']);
	            if(journal_key.length > 0){
	            	var journal_summary_data = order.get_sales_summary_vals()['journal_details'];
	            } else {
	            	var journal_summary_data = false;
	            }
	            var sales_key = Object.keys(order.get_sales_summary_vals()['salesmen_details']);
	            if(sales_key.length > 0){
	            	var sales_summary_data = order.get_sales_summary_vals()['salesmen_details'];
	            } else {
	            	var sales_summary_data = false;
	            }
	            var total = Object.keys(order.get_sales_summary_vals()['summary_data']);
	            if(total.length > 0){
	            	var total_summary_data = order.get_sales_summary_vals()['summary_data'];
	            } else {
	            	var total_summary_data = false;
	            }
	            var receipt = "";
	            receipt = QWeb.render('PaymentSummaryReport',{
	                widget:this,
	                order: order,
	                receipt: order.export_for_printing(),
	                journal_details: journal_summary_data,
	                salesmen_details: sales_summary_data,
	                total_summary : total_summary_data
	            })
	            this.$('.pos-receipt-container').html(receipt);
        } else{
                this._super();
            }
        },
    });
 });