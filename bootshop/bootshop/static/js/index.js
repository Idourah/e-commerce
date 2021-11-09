function prepareDocument(){
    $("#btnSearch").click(function(){
        var term = $("#search_box").val()
        if (term == "" ||  term == "search"){
            alert("Enter search term.");
        }
        else{
            url = "/catalog/search/";
            $.ajax({
                    url:url,
                    type:'GET',
                    dataType:'json',
                    data:{
                       q : term
                    },
                    beforeSend: function(){
                        $(".spinner-border").removeClass("hidden")
                       $(".card-container > div ").remove()
                    },
                    success: function(res){
                        $("#search_box").val("")
                        const data = res.products;
                        appendProductCard(data);
                    },
                    complete:function(){
                       $(".spinner-border").addClass('hidden')
                    }
                 });
        }

    });
}
$(document).ready(prepareDocument);

function appendProductCard(data){

 data.forEach(prod => {
    $(".card-container").append(`
      <div class="col-sm-6 col-md-6 col-lg-4 col-xl-4">
        <div class="products-single fix shadow" style="border:1px solid gainsboro">
            <div class="box-img-hover">
                <div class="type-lb">
                    <p class="sale bg-dark">Sale</p>
                </div>
                <img src="/static/media/images/${prod.image}" class="img-fluid" alt="Image" style="height:150px">
                <div class="mask-icon">
                    <a class="cart bg-info" href="{{ prod.get_absolute_url }}">view detail</a>
                </div>
            </div>
            <div class="why-text">
                <h4>${prod.name}</h4>
                <h5> ${prod.price}$</h5>
            </div>
    </div>
    </div>
    `)

});
}