$(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();

        var address=$("[name='shipping_address']").val();
        var name=$("[name='name']").val();
        var state=$("[name='state']").val();
        var phone=$("[name='phone']").val();
        var pincode=$("[name='pincode']").val();

        $.ajax({
            type: "GET",
            url: "/proceed-to-pay",
            success: function (response) {
                console.log(response)
            }
        });
        var options = {
            "key": "rzp_test_7oJYsPZVdNJar5", // Enter the Key ID generated from the Dashboard
            "amount": "{{amount}}", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "MILATOS",
            "description": "puchase Transaction",
            "image": "https://example.com/your_logo",
            "order_id": "{{payment.id}}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response) {
                alert(response.razorpay_payment_id);
                alert(response.razorpay_order_id);
                alert(response.razorpay_signature)
            },
            "prefill": {
                "name": "Gaurav Kumar",
                "email": "gaurav.kumar@example.com",
                "contact": "9000090000"
            },
            "notes": {
                "address": "Razorpay Corporate Office"
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
    });
});