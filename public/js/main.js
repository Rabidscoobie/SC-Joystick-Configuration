// Google Analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                        })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
ga('create', 'UA-80632859-1', 'auto');
ga('send', 'pageview');


$( document ).ready(function() {
  
  // build the nav items
  $(".page h1, .page h2").each(function(i) {
    var current = $(this);
    spaces = ""
    for (i = 1; i < parseInt(current.get(0).tagName.replace('H',''), 10); i++){spaces += "&nbsp;&nbsp;&nbsp;";}
    $(".sidebar-nav").append("<a class='sidebar-nav-item " + current.get(0).tagName.replace('H','menu_level_') + "' href='#" + current.attr('id') + "'>" + spaces +
                             current.html() + "</a>");
  });
  
  // smooth scrolling to local anchors
  $('a[href*=#]').on('click', function(event){     
    event.preventDefault();
    $('html, body').animate({
      scrollTop: $( $.attr(this, 'href') ).offset().top - 10
    }, 500);
  });
  
  // all external links in new window (except repo download links)
  $('a').each(function() {
    var a = new RegExp('/' + window.location.host + '/');
    if ((!a.test(this.href)) && (!this.attr("title").includes("Download"))) {
      $(this).attr('target','_blank')
    }
  });
  
  // external links tracked by Google Analytics
  $('a').click(function () {
    var a = new RegExp('/' + window.location.host + '/');
    if (!a.test(this.href)) {
      if (this.attr("title").includes("Download")){
        ga('send', 'event', 'download', 'click', this.attr("title"));
      } 
      else {
        ga('send', 'event', 'outbound', 'click', this.attr("title"));
      }
    }
  });
  
  
  // close sidebar on anchor selection
  $(".sidebar-nav a").click(function() {
    $(".sidebar-toggle").click();
    return true;
  });

  // add captions under images
  $(".page img").after(function() {
    var caption = $(this).attr('alt');
    return '<p class="caption"><span>' + caption + '</span></p>';
  });
  
  // wrap images in a.gallery tags
  $(".page img").wrap(function() {
    return "<a class='gallery' href='" + $( this ).prop('src') + "'></div>";
  });

  // add captions in featherlight gallery
  $.featherlightGallery.prototype.afterContent = function() {
    var caption = this.$currentTarget.find('img').attr('alt');
    this.$instance.find('.caption').remove();
    this.$instance.find('.featherlight-content').append('<div class="caption"><span>' + caption + '</span></div>')
  };

  
  // setup lightbox for all a.gallery
  $('.page a.gallery').featherlightGallery({
    previousIcon: '«',
    nextIcon: '»',
    galleryFadeIn: 300,
    openSpeed: 300
  });

});
