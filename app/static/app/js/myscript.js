// $('#slider1, #slider2, #slider3').owlCarousel({
//     loop: true,
//     margin: 20,
//     responsiveClass: true,
//     responsive: {
//         0: {
//             items: 2,
//             nav: false,
//             autoplay: true,
//         },
//         600: {
//             items: 4,
//             nav: true,
//             autoplay: true,
//         },
//         1000: {
//             items: 6,
//             nav: true,
//             loop: true,
//             autoplay: true,
//         }
//     }
// })

// $('.plus-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this.parentNode.children[2] 
//     $.ajax({
//         type:"GET",
//         url:"/pluscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             eml.innerText=data.quantity 
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount
//         }
//     })
// })

// $('.minus-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this.parentNode.children[2] 
//     $.ajax({
//         type:"GET",
//         url:"/minuscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             eml.innerText=data.quantity 
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount
//         }
//     })
// })


// $('.remove-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this
//     $.ajax({
//         type:"GET",
//         url:"/removecart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount
//             eml.parentNode.parentNode.parentNode.parentNode.remove() 
//         }
//     })
// })


// $('.plus-wishlist').click(function(){
//     var id=$(this).attr("pid").toString();
//     $.ajax({
//         type:"GET",
//         url:"/pluswishlist",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             //alert(data.message)
//             window.location.href = `http://localhost:8000/product-detail/${id}`
//         }
//     })
// })


// $('.minus-wishlist').click(function(){
//     var id=$(this).attr("pid").toString();
//     $.ajax({
//         type:"GET",
//         url:"/minuswishlist",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             window.location.href = `http://localhost:8000/product-detail/${id}`
//         }
//     })
// })



// // Function to get CSRF token from the hidden input field
// function getCSRFToken() {
//     return document.getElementById("csrf_token").value;
// }

// // Handle increasing quantity
// $('.plus-cart').click(function() {
//     var id = $(this).attr("pid").toString();
//     var quantityElement = document.getElementById("quantity-" + id);

//     $.ajax({
//         type: "POST",
//         url: "/pluscart/",
//         data: {
//             prod_id: id
//         },
//         headers: {
//             "X-CSRFToken": getCSRFToken()  // Include CSRF token in request header
//         },
//         success: function(data) {
//             console.log("data =", data);
//             quantityElement.innerText = data.quantity;
//             document.getElementById("amount").innerText = "Rs. " + data.amount;
//             document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;
//         }
//     });
// });

// Function to get CSRF token from the hidden input field
function getCSRFToken() {
    return document.getElementById("csrf_token").value;
}

// Handle Increase Quantity
$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Get product ID
    var eml = $(this).closest(".my-3").find(".quantity")[0]; // Find quantity element

    $.ajax({
        type: "POST", // Ensure it's a POST request
        url: "/pluscart/",
        headers: { "X-CSRFToken": getCSRFToken() }, // CSRF token for security
        data: { prod_id: id },
        success: function(data) {
            eml.innerText = data.quantity; // Update quantity
            $("#amount").text("Rs. " + data.amount); // Update total amount
            $("#totalamount").text("Rs. " + data.totalamount);
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
});


// Handle Decrease Quantity
$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString(); // Get product ID
    var eml = $(this).closest(".my-3").find(".quantity")[0]; // Select the correct quantity element

    $.ajax({
        type: "GET", // Ensure it's a GET request as defined in views.py
        url: "/minuscart/",
        data: { prod_id: id },
        success: function(data) {
            if (data.quantity > 0) {
                eml.innerText = data.quantity; // Update quantity text
            } else {
                location.reload(); // Reload the page if quantity reaches 0
            }
            // Update price details
            $("#amount").text("Rs. " + data.amount);
            $("#totalamount").text("Rs. " + data.totalamount);
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
        }
    });
});



// // Handle Remove Item
// $('.remove-cart').click(function() {
//     var id = $(this).attr("pid").toString(); // Get product ID
//     var eml = $(this).closest(".row"); // Select the closest cart item row

//     $.ajax({
//         type: "POST", // Use POST instead of GET
//         url: "/removecart/",
//         headers: { "X-CSRFToken": getCSRFToken() }, // Add CSRF token
//         data: { prod_id: id },
//         success: function(data) {
//             if (data.amount === 0) {
//                 location.reload(); // Reload page if cart is empty
//             } else {
//                 $("#amount").text("Rs. " + data.amount); // Update total amount
//                 $("#totalamount").text("Rs. " + data.totalamount);
//                 eml.fadeOut(500, function() { $(this).remove(); }); // Smoothly remove the item
//             }
//         },
//         error: function(xhr, status, error) {
//             console.error("Error:", error);
//         }
//     });
// });

// Handle Remove Item
// $('.remove-cart').click(function() {
//     var id = $(this).data("pid").toString();
//     var eml = this;

//     $.ajax({
//         type: "GET",
//         url: "/removecart/",
//         data: { prod_id: id },
//         success: function(data) {
//             location.reload();
//         }
//     });
// });
