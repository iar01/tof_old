$(function () {
  $('.category-tile').click(function () {
    $('.category-info-' + this.dataset.categoryId).modal();
  });

  $('#direct_upload input[type="file"]').change(function (e, data) {
        var src = URL.createObjectURL(e.target.files[0]);
        $('.imagepreview img').attr('src', src);
        $('.imagepreview').show();
        $('#btn-upload').click();
      }
  );

  $('#btn-upload').click(function () {
    $('.status_value').text('Uploading...');
    $.ajax({
      url: '/feeds/upload_image/',
      type: "POST",
      data: new FormData(this.form),
      contentType: false,
      cache: false,
      processData: false,
      success: function (data) {
        $('.status_value').text('');
        $('.imagepreview img').attr('src', data.src);
        $('#btn-upload').hide();
        $('.btn-filechose').hide();
        $('#dialog input[name="image"]').val(data.src);
      }
    });
  });

  $(".btn-compose").click(function () {
    if ($("#dialog").hasClass("composing")) {
      $("#dialog").removeClass("composing");
      $("#dialog").slideUp();
    }
    else {
      $("#dialog").addClass("composing");
      $("#dialog").slideDown(400, function () {
        $("#dialog textarea").focus();
      });
    }
  });

  function clear_compose() {
    $("#dialog textarea").val("");
    $('.status_value').text('');
    $('.imagepreview img').attr('src', '');
    $('#btn-upload').hide();
    $('.btn-filechose').show();
    $('.imagepreview').hide();
    $('#dialog input[name="image"]').val('');
    $('#direct_upload input[type="file"]').val('');
  }

  $(".btn-cancel-compose").click(function () {
    clear_compose();
    $("#dialog").slideUp();
  });

  //$(".btn-post").click(function () {
  //    var last_feed = $(".stream li:first-child").attr("feed-id");
  //    if (last_feed == undefined) {
  //        last_feed = "0";
  //    }
  //    $("#compose-form input[name='last_feed']").val(last_feed);
  //    $.ajax({
  //        url: '/competitions/competition/' +  + '/post/',
  //        data: $("#compose-form").serialize(),
  //        type: 'post',
  //        cache: false,
  //        success: function (data) {
  //            $("ul.stream").prepend(data);
  //            $("#dialog").slideUp();
  //            $("#dialog").removeClass("composing");
  //            clear_compose();
  //            hide_stream_update();
  //        }
  //    });
  //});


  $(".entry").on("click", ".like", function () {
    var entryId = $(this).closest(".entry").data().entryId,
        csrf = $('.csrf-holder').data().csrf;

    $.ajax({
      url: '/competitions/like_entry/',
      data: {
        'entry_id': entryId,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $('.likes').html(data.likes);
      }
    });
    return false;
  });

  $('#entry-form').submit(function (event) {
    var postType = $(this).data().type;

    if (postType == 'img' && !$('#dialog input[name="image"]').val()) {
      $.niftyNoty({
        type: "danger",
        container: "floating",
        title: "Empty fields",
        message: "Please upload image",
        closeBtn: false,
        timer: 5000
      });
      event.preventDefault();
      return false;
    }

    if (postType == 'txt' && !$('#dialog textarea[name="post"]').val()) {
      $.niftyNoty({
        type: "danger",
        container: "floating",
        title: "Empty fields",
        message: "Please write something",
        closeBtn: false,
        timer: 5000
      });
      event.preventDefault();
      return false;
    }

    if (postType == 'vid' && !$('#dialog input[name="video_url"]').val()) {
      $.niftyNoty({
        type: "danger",
        container: "floating",
        title: "Empty fields",
        message: "Please upload video file",
        closeBtn: false,
        timer: 5000
      });
      event.preventDefault();
      return false;
    }

  });

  $(".stream").on("click", ".comment", function () {
    var post = $(this).closest(".post");
    if ($(".comments", post).hasClass("tracking")) {
      $(".comments", post).slideUp();
      $(".comments", post).removeClass("tracking");
    }
    else {
      $(".comments", post).show();
      $(".comments", post).addClass("tracking");
      $(".comments input[name='post']", post).focus();
      var feed = $(post).closest("li").attr("feed-id");
      $.ajax({
        url: '/feeds/comment/',
        data: {'feed': feed},
        cache: false,
        beforeSend: function () {
          $("ol", post).html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
        },
        success: function (data) {
          $("ol", post).html(data);
          $(".comment-count", post).text($("ol li", post).not(".empty").length);
        }
      });
    }
    return false;
  });

  $(".stream").on("keydown", ".comments input[name='post']", function (evt) {
    var keyCode = evt.which ? evt.which : evt.keyCode;
    if (keyCode == 13) {
      var form = $(this).closest("form");
      var container = $(this).closest(".comments");
      var input = $(this);
      $.ajax({
        url: '/feeds/comment/',
        data: $(form).serialize(),
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(input).val("");
        },
        success: function (data) {
          $("ol", container).html(data);
          var post_container = $(container).closest(".post");
          $(".comment-count", post_container).text($("ol li", container).length);
        }
      });
      return false;
    }
  });

  // $(".stream").on("click", ".like", function () {
  //   var li = $(this).closest("li");
  //   var feed = $(li).attr("feed-id");
  //   var csrf = $(li).attr("csrf");
  //   $.ajax({
  //     url: '/feeds/like/',
  //     data: {
  //       'feed': feed,
  //       'csrfmiddlewaretoken': csrf
  //     },
  //     type: 'post',
  //     cache: false,
  //     success: function (data) {
  //       if ($(".like", li).hasClass("unlike")) {
  //         $(".like", li).removeClass("unlike");
  //         // $(".like .text", li).text("Like");
  //         $(".like .text", li).text("thumb_up");
  //       }
  //       else {
  //         $(".like", li).addClass("unlike");
  //         // $(".like .text", li).text("Unlike");
  //         $(".like .text", li).text("thumb_down");
  //       }
  //       // $(".like .like-count", li).text(data);
  //       $(".like .text", li).attr("data-badge", data);
  //     }
  //   });
  //   return false;
  // });

  $('#video_upload input[type="file"]').change(function (e, data) {
        var src = URL.createObjectURL(e.target.files[0]);
        //$('.videopreview source').attr('src', src);
        $('.videopreview').show();
        $('.videopreview video').html('<source src="' + src + '" type="video/mp4"></source>');
        $('#btn-video-upload').click();
      }
  );

  $('#btn-video-upload').click(function () {
    $('.status_value').text('Uploading...');
    $.ajax({
      url: '/feeds/upload_video/',
      type: "POST",
      data: new FormData(this.form),
      contentType: false,
      cache: false,
      processData: false,
      success: function (data) {
        $('.status_value').text('');
        //$('.videopreview source').attr('src', data.src);
        $('.videopreview video').html('<source src="/media/video/' + data.src + '" type="video/mp4"></source>');
        $('.videopreview').show();
        $('#btn-video-upload').hide();
        $('.btn-filechose').hide();
        $('#dialog input[name="video_url"]').val(data.src);
      },
      error: function(data){
        $('.status_value').text('Error. Please reload page and try again.');
        $('#video_upload input[type="file"]').val('');
        console.error(data);
      }
    });
  });

  $("#content-container").on("mouseenter", "ul.stream li", function (event) {
    var li = $(this);
    $(li).children(".post").children(".remove-feed").show();
  });

  $("#content-container").on("mouseleave", "ul.stream li", function (event) {
    var li = $(this);
    $(li).children(".post").children(".remove-feed").hide();
  });

  $("ul.stream").on("mouseenter", "li div.post div.comments ol li", function (event) {
    var li = $(this);
    $(li).children(".remove-feed").show();
  });

  $("ul.stream").on("mouseleave", "li div.post div.comments ol li", function (event) {
    var li = $(this);
    $(li).children(".remove-feed").hide();
  });

  // $("ul.stream").on("click", ".remove-feed", function () {
  //   var a = $(this).attr("data-remove"); //new
  //   var li = $('li[feed-id =' + a + ']');
  //   // var li = $(this).closest("li");
  //   var feed = $(li).attr('feed-id');
  //   var csrf = $(li).attr("csrf");
  //   $.ajax({
  //     url: '/feeds/remove/',
  //     data: {
  //       'feed': feed,
  //       'csrfmiddlewaretoken': csrf
  //     },
  //     type: 'post',
  //     cache: false,
  //     success: function (data) {
  //       location.reload();
  //     }
  //   });
  // });

  // $('.feed_edit_btn').on('click', function () {    
  //   $(this).closest('.post').find('.feed_edit_form').toggle('slow');
  // });
});
