
<!DOCTYPE html>

<html lang="en">
<head><meta charset="utf-8"/><base href="./"/><script src="local-preview.js"></script>
<!-- Google tag (gtag.js) -->
<!-- Google Tag Manager -->
<!-- End Google Tag Manager -->
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="images/favicon.png" rel="shortcut icon" type="image/png"/>
<link href="assets/external/cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"/>
<link href="assets/external/cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.carousel.min.css" rel="stylesheet"/>
<script src="assets/external/cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
<link href="assets/external/cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/assets/owl.theme.default.min.css" rel="stylesheet"/>
<link href="assets/external/cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" rel="stylesheet"/>
<link href="css/style.css" rel="stylesheet"/>
<script src="assets/external/cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js"></script>
<!-- Fontawesome CSS -->
<link href="asco-console/assets/css/font-awesome.min.css" rel="stylesheet"/>
<!-- Lineawesome CSS -->
<link href="asco-console/assets/css/line-awesome.min.css" rel="stylesheet"/>
<style>
 section{
    max-width:100vw !important;
    overflow-x:hidden !important;
    height:fit-content;
    overflow-y:hidden;
}
.navbar-toggler:focus,
.navbar-toggler {
    outline: none;
    border: none;
    box-shadow: none;
}

.navbar-toggler-icon {
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba(255, 255, 255, 1)' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

.resource-menu,
.about-menu,
.applications-menu,
.products-menu,
.media-menu {
    display: none;
    position: fixed;
    top: 72px;
    left: 0;
    width: 100%;
    max-width: 100%;
    bottom: 0px;
    background: #0006;
    z-index: 99999;
}

.resource-menu.active,
.about-menu.active,
.applications-menu.active,
.products-menu.active,
.media-menu.active {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
}

.firstmenulist,
.secondmenulist,
.productsdetails {
    height: cals(100vh - 70px);
    transform: translateX(-200%);
    transition: all .5s ease-in-out;
    padding: 40px 50px;
    overflow-y:auto;
}

.firstmenulist.active {
    transform: translateX(0%);
    transition: all .5s ease-in-out;
    background: #fff;
    position: relative;
    z-index: 100;
}

.secondmenulist.active,
.productsdetails.active {
    transform: translateX(0%);
    transition: all .5s ease-in-out;
    background: #fff;
    border-left: 1px solid #555;
    position: relative;
    z-index: 90;
}

.productsdetails.active,
.productsdetails {
    z-index: 80;
}

.menuitems {
    padding: 10px 0px;
    border-top: 1px solid #555;
    font-family: "Swis721 Cn LT", sans-serif;
    color: #555;
}

.menuitems>*,
.menuitems>*>* {
    font-family: "Swis721 Cn LT", sans-serif;
    color: #555;
}

.menusets button,
.menuitems button {
    border: none;
    background: none;
    padding: 10px 0px;
    text-align: left;
}

.menuitems.active button {
    color: #000 !important;
}


.menuitems .innermenu {
    height: 0px !important;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.menuitems.active .innermenu {
    height: fit-content !important;
    padding-bottom: 10px;
}

.menuitems .innermenu a.active {
    color: var(--prime);
}

.rounded-full-badge {
    padding: 10px;
    border-radius: 50%;
    background: var(--sec);
    aspect-ratio: 1;
    display: grid;
    place-items: center;
    color: #fff;
    width: fit-content;
    font-size: 16px;
}

.menusets button {
    border: none;

}

.menusets,
.productitem {
    display: none;
    transition: all .5s ease-in-out;
}

.menusets.active,
.productitem.active {
    display: flex;
    flex-direction: column;
    gap: 1px;
    overflow: hidden;
    transition: all .5s ease-in-out;
}

.menusets.active button {
    padding: 13px 0px;
    border-top: 1px solid #555;
    font-family: "Swis721 Cn LT", sans-serif;
}

.menuitems .toggler:after {
    display: inline-block;
    margin-left: .255em;
    vertical-align: .255em;
    content: "";
    border-top: .3em solid;
    border-right: .3em solid transparent;
    border-bottom: 0;
    border-left: .3em solid transparent;
}

.menuitems.active .toggler:after {
    transform: rotate(180deg)
}

.menusets button.active,
.innermenu button.active {
    color: var(--prime) !important;
}
.secondmenulist .closemenu,
.productsdetails .closemenu{
    display:none;
}
.secondmenulist.active .closemenu,
.productsdetails.active .closemenu{
    display:block;
}

@media (max-width:800px){
    .resource-menu.active,
.about-menu.active,
.media-menu.active,
.applications-menu.active,
.products-menu.active {
    display: flex;
    flex-direction:column;
    overflow-y:auto;
}

.firstmenulist,
.secondmenulist,
.productsdetails {
    padding: 30px;
    overflow-y:visible;
    position:absolute !important;
    top:0;
    width:100%;
    height:100%;
    overflow-y:auto;
}
.secondmenulist{
    z-index:102 !important;
}
.productsdetails{
  z-index:104 !important;  
}
}
</style> <title>Contact HI TECH | Get in Touch for Building Solutions and Support</title>
<meta and="" are="" contact="" content="Need assistance or have inquiries about HI TECH’s building solutions? Contact us today for expert support, product information, and personalized service. We're here to help with all your construction needs." easier="" elements="" find="" for="" get="" hi-tech="" improve="" it="" making="" name="description" need."="" page="" performance,="" seeking="" seo="" support="" tailored="" the="" these="" they="" to="" users="" with=""/>
<meta content="Contact HI TECH, get in touch, building materials support, customer service, construction solutions inquiries, HI TECH contact information, reach HI TECH" name="keywords"/>
<style>
    .grid {
        display: grid;
        grid-template-columns: 5fr 6fr;
    }

    input,
    select,
    textarea {
        background: #ECECF7;
        min-height: 50px;
        width: 100%;
        outline: none;
        border: none;
        padding: 6px 14px;
    }

    textarea {
        margin-bottom: 10px;
        padding: 16px;
    }

    .cont-top-sec {
        position: relative;
    }

    .cont-top-sec img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 0;
    }

    .cont-top-sec .grid {
        position: relative;
        z-index: 1;
        background: #6C016B99;
    }

    .map-container {
        width: 100%;
        height: 400px;
        border-radius: 8px;
        border: 5px solid #fff;
        box-shadow: 0 4px 30px 0 rgba(0, 0, 0, .05)
    }

    .map-container iframe {
        width: 100%;
        height: 100%
    }

    .custscroll::-webkit-scrollbar {
        width: 6px;
    }

    .custscroll::-webkit-scrollbar-track {
        background: #cecece;
        border-radius: 10px;
    }

    .custscroll::-webkit-scrollbar-thumb {
        background-color: var(--prime);
        border-radius: 10px;
    }
    .fs-70{
        font-size: 70px;
    }
    
    @media(max-width:768px){
          .grid {
        display: grid;
        grid-template-columns: 1fr;
    }
    
     .fs-70{
        font-size: 30px;
    }
    
    .border-end{
        border:none!important;
    }
    }
    </style>
</head>
<body>
<style>
    .searchmodal {
        z-index: 99999;
        position: fixed;
        top: 70px;
        left: 0;
        right: 0;
        bottom: 0px;
        background: #0006;
        display: none;
    }

    .searchmodal form {
        display: grid;
        grid-template-columns: 1fr 50px;
    }

    .searchmodal form input::placeholder {
        color: #0009;
    }
</style>
<header>
<nav class="navbar navbar-expand-lg px-xl-5">
<div class="container-fluid px-3 py-md-1">
<a class="navbar-brand" href="index.html"><img alt="" src="images/svg/logo.svg"/></a>
<button aria-expanded="false" class="navbar-toggler" data-bs-target="#navbarSupportedContent" data-bs-toggle="collapse" type="button">
<span class="navbar-toggler-icon text-white"></span>
</button>
<div class="collapse navbar-collapse mt-3 mt-md-0" id="navbarSupportedContent">
<ul class="navbar-nav ms-auto">
<li class="nav-item">
<a class="nav-link about-listing" href="javascript:void();">About Us</a>
</li>
<li class="nav-item">
<a class="nav-link product-listing" href="javascript:void();">Product Listing</a>
</li>
<li class="nav-item">
<a class="nav-link" href="application/index.html">Application Areas</a>
</li>
<li class="nav-item">
<a class="nav-link resource-listing" href="javascript:void();">Knowledge Center</a>
</li>
<li class="nav-item">
<a class="nav-link" href="resources/index.html">Resources</a>
</li>
<li class="nav-item">
<a class="nav-link media-listing" href="javascript:void();">Media</a>
</li>
<li class="nav-item">
<a class="nav-link" href="contact/index.html">Contact Us</a>
</li>
<li class="nav-item">
<a class="nav-link" href="career/index.html">Life At HI TECH</a>
</li>
<li class="nav-item">
<a class="nav-link search-modal" href="javascript:void();">
<img alt="gg" class="img-fluid" src="images/svg/search.svg" width="23px"/>
</a>
</li>
</ul>
</div>
</div>
</nav>
</header>
<div class="searchmodal d-none" id="searchModal">
<form action="#" class="bg-white w-100 px-3 px-md-5 py-1" method="get">
<input id="" name="search" placeholder="Search Product" style="min-height:40px; background:transparent; outline:none; border:none" type="search"/>
<button class="bg-transparent border-0" style="padding:4px; filter:brightness(0%)"><img alt="" class="img-fluid" src="images/svg/search.svg" width="25px"/></button>
</form>
</div>
<div class="products-menu">
<div class="firstmenulist">
<button class="closemenu fs-5">×</button>
<h3 class="mb-4 d-flex gap-2">See All <span class="rounded-full-badge-remove text-sec"></span></h3>
<div class="menuitems">
<button class="toggler"><a href="products/walling-solutions/index.html">WALLING SOLUTIONS</a></button>
<div class="innermenu">

<button data-toggle="menuset20"><a href="products/walling-solutions/masonry-mortars/index.html">Masonry Mortars</a></button>
<button data-toggle="menuset21"><a href="products/walling-solutions/ready-mix-plasters/index.html">Ready Mix Plasters</a></button>




</div>
</div>


<div class="menuitems">
<button class="toggler">STRUCTURAL REPAIRS, SEALANTS AND GROUTS</button>
<div class="innermenu">


<button data-toggle="menuset12">Non Shrink Grouts</button>

<button data-toggle="menuset17">Floor Hardener</button>





</div>
</div>

</div>
<div class="secondmenulist">
<button class="closemenu fs-5">×</button>
<div class="menusets" id="menuset12">
<h4 class="fs-2 mb-4">Non Shrink Grouts</h4>
<button data-toggle="product58">ASCOGROUT<sup>®</sup>65</button>
</div>
<div class="menusets" id="menuset17">
<h4 class="fs-2 mb-4">Floor Hardener</h4>
<button data-toggle="product77">ASCOTOP FH 111</button>
</div>
<div class="menusets" id="menuset20">
<h4 class="fs-2 mb-4">Masonry Mortars</h4>
<button data-toggle="product22">ASCOFIX BJM/TBM</button>
</div>
<div class="menusets" id="menuset21">
<h4 class="fs-2 mb-4">Ready Mix Plasters</h4>
<button data-toggle="product25">READY MIX MORTAR</button>
</div>
</div>
<div class="productsdetails">
<button class="closemenu fs-5">×</button>
<div class="productitem" id="product22">
<!--<img src="https://hi-tech.in/uploads/images/1726050486-1_crop.webp" alt="" class="w-75 mx-auto img-fluid d-block">-->
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726050486-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOFIX BJM/TBM</h5>
<p>ASCOFIX BJM / TBM  is a pre-mixed, self-curing &amp; non-shr...</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/walling-solutions/masonry-mortars/ascofix-bjm/index.html">View
                    Products</a>
</div>
<div class="productitem" id="product25">
<!--<img src="https://hi-tech.in/uploads/images/1726054121-1_crop.webp" alt="" class="w-75 mx-auto img-fluid d-block">-->
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726054121-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">READY MIX MORTAR</h5>
<p>READY MIX MORTAR is a pre-mixed cement-based solution that substitutes the trad...</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/walling-solutions/ready-mix-plasters/ready-mix-mortar/index.html">View
                    Products</a>
</div>
<div class="productitem" id="product58">
<!--<img src="https://hi-tech.in/uploads/images/1724487756-1_crop.webp" alt="" class="w-75 mx-auto img-fluid d-block">-->
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1724487756-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOGROUT<sup>®</sup>65</h5>
<p>ASCOGROUT® 65 is a specially modified multipurpose, high-low, non-shrink &amp; ce...</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/structural-repairs-sealants-and-grouts/non-shrink-grouts/aascogrout65/index.html">View
                    Products</a>
</div>
<div class="productitem" id="product77">
<!--<img src="https://hi-tech.in/uploads/images/1726059398-1_crop.webp" alt="" class="w-75 mx-auto img-fluid d-block">-->
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726059398-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOTOP FH 111</h5>
<p>ASCOTOP FH 111 is a mixture of finely graded non-metallic quartz
aggregates, p...</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/structural-repairs-sealants-and-grouts/floor-hardener/ascotop-fh-111/index.html">View
                    Products</a>
</div>
</div>
</div>
<div class="applications-menu">
<div class="firstmenulist">
<button class="closemenu fs-5">×</button>
<h3 class="mb-4 d-flex gap-2">See All <span class="rounded-full-badge">4</span></h3>
<div class="menuitems">
<button class="toggler">WALLING SOLUTIONS</button>
<div class="innermenu">
<button data-toggle="amenuset20">Masonry Mortars</button>
<button data-toggle="amenuset21">Ready Mix Plasters</button>
</div>
</div>
<div class="menuitems">
<button class="toggler">STRUCTURAL REPAIRS, SEALANTS AND GROUTS</button>
<div class="innermenu">
<button data-toggle="amenuset12">Non Shrink Grouts</button>
<button data-toggle="amenuset17">Floor Hardener</button>
</div>
</div>
</div>
<div class="secondmenulist">
<button class="closemenu fs-5">×</button>
<div class="menusets" id="amenuset12">
<h4 class="fs-2 mb-4">Non Shrink Grouts</h4>
<button data-toggle="aproduct58">ASCOGROUT<sup>®</sup>65</button>
</div>
<div class="menusets" id="amenuset17">
<h4 class="fs-2 mb-4">Floor Hardener</h4>
<button data-toggle="aproduct77">ASCOTOP FH 111</button>
</div>
<div class="menusets" id="amenuset20">
<h4 class="fs-2 mb-4">Masonry Mortars</h4>
<button data-toggle="aproduct22">ASCOFIX BJM/TBM</button>
</div>
<div class="menusets" id="amenuset21">
<h4 class="fs-2 mb-4">Ready Mix Plasters</h4>
<button data-toggle="aproduct25">READY MIX MORTAR</button>
</div>
</div>
<div class="productsdetails">
<button class="closemenu fs-5">×</button>
<div class="productitem" id="aproduct22">
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726050486-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOFIX BJM/TBM</h5>
<p>ASCOFIX BJM / TBM  is a pre-mixed, self-curing &amp; non-shr</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/walling-solutions/masonry-mortars/ascofix-bjm/index.html">View
                    Products</a>
</div>
<div class="productitem" id="aproduct25">
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726054121-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">READY MIX MORTAR</h5>
<p>READY MIX MORTAR is a pre-mixed cement-based solution that substitutes the trad</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/walling-solutions/ready-mix-plasters/ready-mix-mortar/index.html">View
                    Products</a>
</div>
<div class="productitem" id="aproduct58">
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1724487756-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOGROUT<sup>®</sup>65</h5>
<p>ASCOGROUT® 65 is a specially modified multipurpose, high-low, non-shrink &amp; ce</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/structural-repairs-sealants-and-grouts/non-shrink-grouts/aascogrout65/index.html">View
                    Products</a>
</div>
<div class="productitem" id="aproduct77">
<img alt="" class="w-75 mx-auto img-fluid d-block" src="uploads/images/1726059398-1_crop.webp"/>
<h5 class="fs-2 mt-4 text-uppercase">ASCOTOP FH 111</h5>
<p>ASCOTOP FH 111 is a mixture of finely graded non-metallic quartz
aggregates, p</p>
<a class="btn-sec text-uppercase d-flex justify-content-center" href="products/structural-repairs-sealants-and-grouts/floor-hardener/ascotop-fh-111/index.html">View
                    Products</a>
</div>
</div>
</div>
<div class="about-menu">
<div class="firstmenulist">
<button class="closemenu fs-5">×</button>
<h3 class="mb-4 d-flex gap-2">About Us</h3>
<div class="menuitems"><a href="about/index.html">Overview</a></div>
<div class="menuitems"><a href="team/index.html">Our Team</a></div>
<div class="menuitems"><a href="clients/index.html">Our Customers</a></div>
</div>
</div>
<div class="media-menu">
<div class="firstmenulist">
<button class="closemenu fs-5">×</button>
<h3 class="mb-4 d-flex gap-2">Media</h3>
</div>
</div>
<div class="resource-menu">
<div class="firstmenulist">
<button class="closemenu fs-5">×</button>
<h3 class="mb-4 d-flex gap-2">Knowledge Center</h3>
<div class="menuitems"><a href="testimonials/index.html">Testimonials</a></div>
<div class="menuitems"><a href="project/index.html">Project Showcases</a></div>
<div class="menuitems"><a href="blog/index.html">Blogs</a></div>
</div>
</div>
<script>
    jQuery(document).ready(function($) {
        $('.search-modal').click(function() {
            $('.applications-menu , .about-menu , .resource-menu , .firstmenulist , .secondmenulist , .productsdetails , .products-menu').removeClass('active');
            $('.searchmodal').toggleClass('d-none');
        });

        // Close search modal if clicked outside the form
        $(document).click(function(event) {
            if (!$(event.target).closest('#searchModal form, .search-modal').length) {
                $('#searchModal').addClass('d-none');
            }
        });

        $('.product-listing').click(function() {
            $('.applications-menu, .about-menu, .resource-menu, .firstmenulist, .secondmenulist, .productsdetails').removeClass('active');
            $('.searchmodal').addClass('d-none');
            $('.products-menu').toggleClass('active');
            setTimeout(function() {
                $('.products-menu .firstmenulist').addClass('active');
            }, 50);
        });

        $('.menuitems .toggler').mouseenter(function() {
            var $parentMenu = $(this).closest('.menuitems');
            $('.menuitems').not($parentMenu).removeClass('active');
            $parentMenu.toggleClass('active');
        });

        $('.innermenu button').mouseenter(function() {
            var toggleId = $(this).data('toggle');
            $('.innermenu button').not(this).removeClass('active');
            $(this).addClass('active');
            $('.secondmenulist').addClass('active');
            $('.menusets').not('#' + toggleId).removeClass('active');
            $('#' + toggleId).addClass('active');
            $('.productitem, .productsdetails, .menusets button').removeClass('active');
        });

        $('.menusets button').mouseenter(function() {
            var togglemenuId = $(this).data('toggle');
            $('.menusets button').not(this).removeClass('active');
            $(this).addClass('active');
            $('.productsdetails').addClass('active');
            $('.productitem').not('#' + togglemenuId).removeClass('active');
            $('#' + togglemenuId).addClass('active');
        });

        // Applications Menu Navigation
        $('.applica-listing').click(function() {
            $('.products-menu, .about-menu, .resource-menu, .firstmenulist, .secondmenulist, .productsdetails').removeClass('active');
            $('.searchmodal').addClass('d-none');
            $('.applications-menu').toggleClass('active');
            setTimeout(function() {
                $('.applications-menu .firstmenulist').addClass('active');
            }, 50);
        });

        // About Menu Navigation
        $('.about-listing').click(function() {
            $('.products-menu, .resource-menu, .firstmenulist, .secondmenulist, .productsdetails, .applications-menu').removeClass('active');
            $('.searchmodal').addClass('d-none');
            $('.about-menu').toggleClass('active');
            setTimeout(function() {
                $('.about-menu .firstmenulist').addClass('active');
            }, 50);
        });

        $('.media-listing').click(function() {
            $('.products-menu, .resource-menu, .firstmenulist, .secondmenulist, .productsdetails, .applications-menu, .about-menu').removeClass('active');
            $('.searchmodal').addClass('d-none');
            $('.media-menu').toggleClass('active');
            setTimeout(function() {
                $('.media-menu .firstmenulist').addClass('active');
            }, 50);
        });

        // Resource Menu Navigation
        $('.resource-listing').click(function() {
            $('.products-menu, .about-menu, .firstmenulist, .secondmenulist, .productsdetails, .applications-menu').removeClass('active');
            $('.searchmodal').addClass('d-none');
            $('.resource-menu').toggleClass('active');
            setTimeout(function() {
                $('.resource-menu .firstmenulist').addClass('active');
            }, 50);
        });

        // Menu Close button
        $('.productsdetails .closemenu').click(function() {
            $('.productsdetails, .productitem').removeClass('active');
        });

        $('.secondmenulist .closemenu').click(function() {
            $('.secondmenulist, .productsdetails, .productitem').removeClass('active');
        });

        $('.firstmenulist .closemenu').click(function() {
            $('.secondmenulist, .productsdetails, .productitem, .products-menu, .applications-menu, .about-menu, .resource-menu, .media-menu').removeClass('active');
        });


        $('.products-menu , .resource-menu , .about-menu').click(function(event) {
            if (!$(event.target).closest('.firstmenulist, .secondmenulist, .productsdetails').length) {
                $('.firstmenulist, .secondmenulist, .productsdetails, .products-menu, .applications-menu, .about-menu, .resource-menu').removeClass('active');
            }
        });

        $('.products-menu').click(function() {
            if (!$('.products-menu').hasClass('active')) {
                $('.firstmenulist, .secondmenulist, .productsdetails, .products-menu, .applications-menu, .about-menu, .resource-menu').removeClass('active');
            }
        });



    });
</script> <main class="bg-light">
<section>
<div class="hero">
<!-- <img src="" alt=""> -->
<div class="content">
<h1>Contact Us</h1>
<p><a href="index.html">Home</a> <i aria-hidden="true" class="fa fa-angle-right" style="padding: 5px;"></i> Contact Us </p>
</div>
</div>
</section>
<section class="position-relative">
<div class="container-fluid px-3 px-lg-5 py-5" data-aos="fade-up">
<div class="cont-top-sec">
<img alt="" src="images/contact/contactpgbg.webp"/>
<div class="grid text-white p-4 p-md-5">
<div class="d-flex flex-column justify-content-center border-end px-md-5 px-sm-3 px-0" data-aos="fade-up">
<h2 class="text-uppercase fs-70">
                                Happy to help you</h2>
</div>
<div class="d-flex flex-column justify-content-center px-md-5 px-sm-3 px-0" data-aos="fade-up">
<p class="fs-7 mb-0 fw-light leadloose">
                                Have questions or need more information about our products and services? We're here to help. Reach out to our service team for any inquiries, and we will respond as quickly as possible. Your satisfaction is our priority.                            </p>
</div>
</div>
</div>
<div class="grid mt-4 pt-3">
<div class="" data-aos="fade-up">
<img alt="" class="img-fluid" src="uploads/images/1720092138-1_crop.jpg"/>
<p class="p-4">
                            Interested in our innovative solutions for your project? We are  ready to assist you with product information, pricing, and orders. Let us help you find the best solutions for your needs.                             <!-- <a href="#" class="text-decoration-underline">Check out our FAQ</a> -->
</p>
</div>
<div class="bg-white h-100 p-4 p-lg-5" data-aos="fade-up">
<div class="px-0 px-sm-3 px-lg-4 px-xl-5">
<h3 class="text-prime text-uppercase fs-1">Drop Us your Enquiry                            </h3>
<form class="d-flex flex-column gap-4 mt-4" id="form" method="post">
<input name="name" placeholder="Full Name" required="" type="text"/>
<input name="email" placeholder="Email ID" required="" type="email"/>
<input name="mobile" placeholder="Phone Number" required="" type="tel"/>
<select name="service" required="">
<option value="">Select</option>
<option value="sale_inquiry">Sale Inquiry</option>
<option value="customer_feedback">Customer Feedback</option>
<option value="other">Other</option>
</select>
<textarea name="message" placeholder="Message" required="" rows="6"></textarea>
<button class="btn-sec" name="submit" type="submit">Submit</button>
</form>
</div>
</div>
</div>
<div class="mt-5 position-relative" data-aos="fade-up">
<img alt="" class="img-fluid object-fit-cover position-relative w-100" src="uploads/images/1727158230-1_crop.webp" style="min-height:300px; object-position:right;"/>
<div class="grid text-white p-5 position-absolute top-0 left-0 w-100 h-100" style="z-index: 3;">
<div class="d-flex flex-column pe-3 px-lg-5 custscroll" style="height:100%; overflow-y:auto">
<h2 class="text-uppercase mb-4">Our Presence </h2>
<h4 class="mb-4 fs-5">HI TECH's commitment to delivering engineered building materials extends across multiple regions in India.                            </h4>
<p><span style="font-size: 0.9375rem;">Expanding beyond Gujarat, HI TECH ventured into Maharashtra and Madhya Pradesh, strategically positioning itself as a multi-state player in the building materials sector. Next ahead in Southern India, from our warehouse in Tamil Nadu, we continue to expand our footprints. This expansion reflects our continuous effort to support local development projects.</span><br/></p> </div>
</div>
</div>
</div>
</section>
<section id="map">
<div class="container-fluid px-3 pb-5 px-lg-5" data-aos="fade-up">
<div class="map-container">
<iframe allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src=" https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3009.003716115144!2d72.833920474139!3d21.14125418390749!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be05128c3528a4b%3A0x459bd437c32bb9ad!2sHI TECH%20Industries%20Pvt%20Ltd!5e1!3m2!1sen!2sin" width="100%">
</iframe>
</div>
</div>
</section>
</main>
<div class="sideicons">
<a class="quickcontact" href="contact/index.html">Quick Enquiry</a>
<a href="https://wa.me/+916352541391" target="_blank"><img alt="" src="images/svg/whatsapp.svg" style="width:35px; height:35px;"/></a>
</div>
<footer class="px-0">
<div class="container text-white">
<div class="row pt-lg-4">
<div class="col-lg-3 col-xl-2 col-md-4 col-sm-6">
<h3 class="text-white fs-5">QUICK LINKS</h3>
<ul class="list-style-none">
<li><a href="index.html">Home</a></li>
<li><a class="about-listing" href="javascript:void();">About Us</a></li>
<li><a class="product-listing" href="javascript:void();">Product Solutions</a></li>
<li><a href="application/index.html">Application Areas</a></li>
<li><a href="resources/index.html">Resources</a></li>
</ul>
</div>
<div class="col-lg-3 col-xl-4 col-md-4 col-sm-6">
<ul class="list-style-none mt-sm-4 pt-2">
<li><a href="blog/index.html">Blogs</a></li>
<li><a href="contact/index.html">Contact Us</a></li>
<li><a href="terms-conditions/index.html">Terms &amp; Conditions</a></li>
<li><a href="privacypolicy/index.html">Privacy Policy</a></li>
</ul>
</div>
<div class="col-lg-3 col-md-4 col-sm-6">
<h3 class="text-white fs-5">LOCATION</h3>
<p class="lead30">HI TECH Industries Pvt Ltd
150, GIDC, Pandesara Road, Laxmi Narayan Nagar, Pandesara GIDC, Udhana, Surat, Gujarat 394221</p>
<a class="text-white text-decoration-underline" href="contact/index.html#map">VIEW MAP</a>
</div>
<div class="col-lg-3 col-md-4 col-sm-6">
<h3 class="text-white fs-5">FOLLOW US</h3>
<div class="d-flex flex-wrap gap-3 mt-3">
<a href="https://www.instagram.com/hi-tech_india/" target="_blank"><img alt="" src="images/svg/icon (1).svg"/></a> <a href="https://www.facebook.com/hi-tech.india" target="_blank"><img alt="" src="images/svg/icon (2).svg"/></a>
<a href="https://x.com/hi-tech" target="_blank"><img alt="" src="images/svg/icon (3).svg"/></a>
<a href="https://www.linkedin.com/company/13391829/admin/feed/posts/" target="_blank"><img alt="" src="images/svg/icon (4).svg"/></a>
<a href="https://youtube.com/@hi-tech" target="_blank"><img alt="" src="images/svg/icon (5).svg"/></a>
</div>
<br/>
<h3 class="text-white fs-5">Phone</h3>
<a href="tel:18005327788">18005327788</a> <!-- / <a href="tel:7486070126">7486070126</a> -->
</div>
</div>
<div class="row">
<div class="col-sm-6">
<div class="subscribe_now">
<form class="subscribe_form">
<div class="input-group">
<input class="form-control" name="subscription_email" placeholder="Enter your email" style="border-radius: 10px; background:#ECECF7;height:50px;" type="text"/>
<span class="input-group-btn">
<button class="btn-sec btn-subscribe" onclick="subscribe()" style="margin-left:10px; border-radius: 10px; padding:8px;" type="button">subscribe</button>
</span>
</div>
</form>
</div>
</div>
</div>
</div>
<div class="w-100 pt-1 bg-sec mt-5">
</div>
<p class="text-center text-sec mt-3 mb-0" style="padding:0; line-height:0;">©2026 HI TECH All Rights Reserved</p>
</footer>
<style>
.cookie-consent {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 15px;
    text-align: center;
    display: none;
    z-index: 1000;
}

.cookie-consent p {
    margin: 0;
    padding: 0 10px;
    display: inline-block;
}

.cookie-consent button {
    background-color: var(--prime);
    color: white;
    border: none;
    padding: 4px 20px;
    cursor: pointer;
    margin-left: 10px;
    border-radius:6px;
    display: inline-block;
}

.cookie-consent button:hover {
    background-color: #fff;
    color: var(--prime);
}
</style>
<div class="cookie-consent" id="cookie-consent">
<p>This website uses cookies to serve content relevant for you and to improve your overall website experience. By continuing to visit this site, you agree to our use of cookies.</p>
<button id="accept-cookies">Accept</button>
</div>
<script>
$(document).ready(function() {
    const cookieConsent = $('#cookie-consent');
    const acceptCookiesButton = $('#accept-cookies');
    if (!localStorage.getItem('cookiesAccepted')) {
        cookieConsent.show();
    }
    acceptCookiesButton.on('click', function() {
        localStorage.setItem('cookiesAccepted', 'true');
        cookieConsent.hide();
    });
});
</script><script src="assets/external/cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script src="assets/external/cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
<script>
$(document).ready(function() {
    AOS.init({
        offset: 150,
        duration: 1200,
        once: true,
    });

    $('.search-modal').click(function() {
        $('#searchModal').show();
    });

    $('.close').click(function() {
        $('.modal').modal('hide');
    });
    // // Products Menu Navigation
    // $('.product-listing').click(function() {
    //     $('.applications-menu').removeClass('active');
    //     $('.about-menu').removeClass('active');
    //     $('.resource-menu').removeClass('active');
    //     $('.firstmenulist').removeClass('active');
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.products-menu').toggleClass('active');
    //     setTimeout(function() {
    //         $('.products-menu .firstmenulist').addClass('active');
    //     }, 50);
    // });

    // $('.menuitems .toggler').click(function() {
    //     var $parentMenu = $(this).closest('.menuitems');
    //     $('.menuitems').not($parentMenu).removeClass('active');
    //     $parentMenu.toggleClass('active');
    // });

    // $('.innermenu button').click(function() {
    //     var toggleId = $(this).data('toggle');
    //     $('.innermenu button').not(this).removeClass('active');
    //     $(this).addClass('active');
    //     $('.secondmenulist').addClass('active');
    //     $('.menusets').not('#' + toggleId).removeClass('active');
    //     $('#' + toggleId).addClass('active');
    //     $('.productitem').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.menusets button').removeClass('active');
    // });

    // $('.menusets button').click(function() {
    //     var togglemenuId = $(this).data('toggle');
    //     $('.menusets button').not(this).removeClass('active');
    //     $(this).addClass('active');
    //     $('.productsdetails').addClass('active');
    //     $('.productitem').not('#' + togglemenuId).removeClass('active');
    //     $('#' + togglemenuId).addClass('active');
    // });

    // // Applications Menu Navigation
    // $('.applica-listing').click(function() {
    //     $('.products-menu').removeClass('active');
    //     $('.about-menu').removeClass('active');
    //     $('.resource-menu').removeClass('active');
    //     $('.firstmenulist').removeClass('active');
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.applications-menu').toggleClass('active');
    //     setTimeout(function() {
    //         $('.applications-menu .firstmenulist').addClass('active');
    //     }, 50);
    // });

    // // AboutMenu Navigation

    // $('.about-listing').click(function() {
    //     $('.products-menu').removeClass('active');
    //     $('.resource-menu').removeClass('active');
    //     $('.firstmenulist').removeClass('active');
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.applications-menu').removeClass('active');
    //     $('.about-menu').toggleClass('active');
    //     setTimeout(function() {
    //         $('.about-menu .firstmenulist').addClass('active');
    //     }, 50);
    // });

    // // ResourceMenu Navigation

    // $('.resource-listing').click(function() {
    //     $('.products-menu').removeClass('active');
    //     $('.about-menu').removeClass('active');
    //     $('.firstmenulist').removeClass('active');
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.applications-menu').removeClass('active');
    //     $('.resource-menu').toggleClass('active');
    //     setTimeout(function() {
    //         $('.resource-menu .firstmenulist').addClass('active');
    //     }, 50);
    // });


    // // Menu Close button
    // $('.productsdetails .closemenu').click(function() {
    //     $('.productsdetails').removeClass('active');
    //     $('.productitem').removeClass('active');
    // });
    // $('.secondmenulist .closemenu').click(function() {
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.productitem').removeClass('active');
    // });
    // $('.firstmenulist .closemenu').click(function() {
    //     $('.secondmenulist').removeClass('active');
    //     $('.secondmenulist').removeClass('active');
    //     $('.productsdetails').removeClass('active');
    //     $('.productitem').removeClass('active');
    //     $('.products-menu').removeClass('active');
    //     $('.applications-menu').removeClass('active');
    //     $('.about-menu').removeClass('active');
    //     $('.resource-menu').removeClass('active');
    // });
});

function subscribe() {
    var subscription_email = $('input[name="subscription_email"]').val().trim();
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(subscription_email) || !subscription_email) {        
        $('input[name="subscription_email"]').closest('.form-control').css('border', '1px solid red');
        return false;
    }    
    $('input[name="subscription_email"]').closest('.form-control').css('border', '#dee2e6');

    var postData = {subscription_email: subscription_email, type: 'subscribe_newsletter'};
    $('.btn-subscribe').html('wait..').attr('disabled',true);    
    $.ajax({
        url: 'ajaxcall.php',
        type: 'POST',
        data: postData,
        dataType: 'json',        
        success: function(res) {
             console.log(res);
            if(res.status === true)
                $('.btn-subscribe').html('Done!').attr('disabled',false);
        },
    });
}

</script>
</body>
<script src="assets/external/cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</html>
<!-- https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3721.285530750741!2d72.83679800000002!3d21.1410323!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be05128c3528a4b%3A0x459bd437c32bb9ad!2sHI TECH%20Industries%20Pvt%20Ltd!5e0!3m2!1sen!2sin!4v1715770382521!5m2!1sen!2sin -->