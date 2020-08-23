$(document).ready(function(){
//    alert('This is to check if js is working');
   var x = window.matchMedia("(max-width: 700px)");

    onLoadCartIn();
    button_events_load();
    function getValue() {
        var current_pull = parseInt($('#mySidepanel').css('transform').split(',')[4]);
        return current_pull
    }

    function open_panel() {
        var translX = getValue();
        if (translX > 0) {
            $("#mySidepanel").css({
                'transform': 'translateX(0)',
                '-webkit-transform': 'translateX(0)',
                '-ms-transform': 'translateX(0)'});

        } else {
            $("#mySidepanel").css({
                'transform': 'translateX(100%)',
                '-webkit-transform': 'translateX(100%)',
                '-ms-transform': 'translateX(100%)'
            });
        }
    }
    // cart panel animation
    
    function button_events_load() {

    $('.openbtn').on('click', function(e){
        e.preventDefault();
        open_panel();
    });

    $('.mobile-add-btn').on('click', function(e){
        e.preventDefault();
        open_panel();
    });

    $('.closebtn').on('click', function(e){
        e.preventDefault();
        $("#mySidepanel").css({
            'transform': 'translateX(100%)',
            '-webkit-transform': 'translateX(100%)',
            '-ms-transform': 'translateX(100%)'
        });      
    });


}

    function plus_minus_button_load() {
        $('.plus').on('click', function(e){
            e.preventDefault();
            name = e.target.dataset.name;
            target = Array.from(e.currentTarget.classList);
            cart_inc_dec(name, target);
        });
        $('.minus').on('click', function(e){
            e.preventDefault();
            name = e.target.dataset.name;
            target = Array.from(e.currentTarget.classList);
            cart_inc_dec(name, target);
        });
        
    }
    // add to cart function
    

    function set_cart_pop(){
        let basket = JSON.parse(localStorage.getItem('basket'));
        pop = 0;
        if (basket) {
            for (const items in basket.items) {
                pop += basket.items[items].quantity
            };
            $('.in-cart').text(pop);
            $('.in-cart').css('display', 'inline-block');
        }
        else {
            $('.in-cart').css('display', 'none');
        }
    }

    $('.add-to-cart').on('click', function(e){
        e.preventDefault();
        let basket = JSON.parse(localStorage.getItem('basket'));
        console.log('Retrieve data-product-code to send to Django server');
        product_code = e.target.dataset.productCode;
        items = basket.items;
        name = ""
        for (const x in items) {
            if (basket.items[x].code == product_code) {
                name = basket.items[x].name;
                console.log(name);
            }
        }

        if (name) {
            add_same_item(name);
        }
        else {
            $.ajax({
                url: 'add_to_cart/',
                method: 'GET',
                dataType: 'json',
                contentType: "application/json; charset=utf-8",
                data: {code : product_code},
                success: function(response){
                    console.log('ajax GET request success');
                    setItemsBasket(response);
                },
                error: function(response){
                    console.log(response);
                }
            });
        }
    });

        $('.place-order').on('click', function(e){
            e.preventDefault();
            const csrftoken = getCookie('csrftoken');
            let basket = JSON.parse(localStorage.getItem('basket'));
            let payment = $('#pay-method option:selected').val();
                $.ajax({
                    url: 'placeorder/',
                    headers: {'X-CSRFToken': csrftoken},
                    method: 'POST',
                    dataType: 'json',
                    contentType: "application/json;charset=utf-8",
                    data: JSON.stringify({
                        products: basket.items,
                        payment : payment,
                    }),
                    success: function(response) {
                        $('#transaction_id_ajax').text("Transaction ID: " + response.transaction_id);
                        $('#payment_type_ajax').text("Payment Type: " + response.payment_type);
                        $('#name_ajax').text("Receiver Name: " + response.name);
                        $('#mobile_ajax').text("Mobile No.: " + response.mobile);
                        $('#placeordermodal').modal('show');
                        localStorage.clear();
                        setTimeout(function(){ window.location = "/store/"; }, 3000);
                    },
                    error: function(response) {
                        console.log(response);
                    }
                });
    });
        
    function onLoadCartIn() {
        let basket_start = JSON.parse(localStorage.getItem('basket'));
        if (basket_start && Object.keys(basket_start.items).length != 0) {
            set_cart_pop()
        } else {
            $('.in-cart').css('display', 'none');
            localStorage.setItem('basket', JSON.stringify({items: {}}));
        }
        updateCartPanel();
    }

    function setItemsBasket(product) {
        let basket = JSON.parse(localStorage.getItem('basket'));

        console.log('adding a new item');
        basket.items[product.name] = product;
        initial_price = basket.items[product.name].price;
        basket.items[product.name].quantity = 1;
        basket.items[product.name].total_price = initial_price; 
        

        localStorage.setItem('basket', JSON.stringify(basket));
        set_cart_pop();
        updateCartPanel();
    }

    function updateCartPanel() {
        $('#update-panel').empty();
        let basket = JSON.parse(localStorage.getItem('basket'));
        let products_basket = basket.items;
        
        for (const items in products_basket) {
            let html =  "<div class='col-12 my-2' id='"+basket.items[items].code+"'>" +
                        "<div class='row'> "+
                            "<div class='col-6 text-center border border-primary d-flex align-items-center'>" +
                                "<img class='m-auto border border-danger' src=" + basket.items[items].images[0].image +">" +
                            "</div>" +
                            "<div class='col-6'> " +
                                "<div class='col-12'> " + basket.items[items].name + " </div> " +
                                    "<div class='col-12  justify-content-between'> " + 
                                        "<div class=''>Quantity:</div>" + 
                                        "<div class=''> " + 
                                            "<a class=' text-light btn btn-primary minus' data-name=\"" + 
                                            basket.items[items].name+ "\" href=''>-</a>" + 
                                            "<span class='mx-3 cart-quantity'>"+basket.items[items].quantity+"</span>" + 
                                            "<a class=' text-light btn btn-primary plus' data-name=\"" +
                                            basket.items[items].name + "\" href=''>+</a>" +
                                        "</div>" + 
                                    "</div>" + 
                                    "<div class='col-12'>" + 
                                        "<span>Total Price: </span>" +
                                        "<span class='currency'>₱</span>" +
                                        "<span class='item_total_price'>" + basket.items[items].total_price + "</span>" +
                                "</div>" +
                            "</div>" +
                        "</div>"+
                        "</div>";
            $('#update-panel').append(html);
        };
        sub_total_update();
        plus_minus_button_load();
    }
    
    function add_same_item(name) {
            let basket = JSON.parse(localStorage.getItem('basket'));
            console.log('Increasing Quantity of ' + basket.items[name].name);
            price = basket.items[name].price;
            basket.items[name].quantity += 1;
            quantity = basket.items[name].quantity;
            basket.items[name].total_price = price*quantity;
            localStorage.setItem('basket', JSON.stringify(basket));
            set_cart_pop();
            updateCartPanel();
    }

    function cart_inc_dec(name, target){
        let basket = JSON.parse(localStorage.getItem('basket'));
        if (target.includes('plus')){
            basket.items[name].quantity += 1;
        }
        else {
            basket.items[name].quantity -= 1;
        }
        price = basket.items[name].price;
        quantity = basket.items[name].quantity;
        basket.items[name].total_price = price*quantity;
        localStorage.setItem('basket', JSON.stringify(basket));
        code_id = '#' + basket.items[name].code;
        div_quantity = code_id + ' .cart-quantity';
        div_t_price = code_id + ' .item_total_price';
        $(div_quantity).text(quantity);
        $(div_t_price).text(basket.items[name].total_price);
        sub_total_update();
        set_cart_pop();
    }

    function sub_total_update() {
        let basket = JSON.parse(localStorage.getItem('basket'));
        let products_basket = basket.items;
        let cart_sub = 0;
        let ship_pay = parseInt($('.ship_fee').text());

        for (const items in products_basket) {
            cart_sub += basket.items[items].total_price;
        }
        let total_pay = cart_sub + ship_pay;
        $('.cart-sub-total').data('sub_total', cart_sub);
        $('.cart-sub-total').text(cart_sub);
        $('.total_payment').text(total_pay);
    }
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    
});



