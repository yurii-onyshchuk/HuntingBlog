$(document).ready(function () {

    $('.menu a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location === link) {
            $(this).parent().addClass('active');
        }
    });
    var $grid = $('.grid').isotope({
        filter: '.popular',
        layoutMode: 'fitRows'
    });

    var filterFns = {
        ium: function () {
            var name = $(this).find('.name').text();
            return name.match(/ium$/);
        }
    };
    $('.filters-button-group').on('click', 'button', function () {
        var filterValue = $(this).attr('data-filter');
        filterValue = filterFns[filterValue] || filterValue;
        $grid.isotope({
            filter: filterValue
        });
    });
    $('.button-group').each(function (i, buttonGroup) {
        var $buttonGroup = $(buttonGroup);
        $buttonGroup.on('click', 'button', function () {
            $buttonGroup.find('.is-checked').removeClass('is-checked');
            $(this).addClass('is-checked');
        });
    });

    // Add to wishlist
    $(document).on('click', '#like', function (e) {
        const comment_id = $(this).attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-url'),
            data: {
                comment_id: comment_id,
                csrfmiddlewaretoken: $('#like-form input[name="csrfmiddlewaretoken"]').attr('data-index', comment_id).val(),
                action: 'post'
            },
            success: function (json) {
                const like_total = document.getElementById("like-total-" + comment_id)
                like_total.innerText = json.like_total

                if (json.like_total > '0') {
                    like_total.style.display = 'inline-block'
                } else {
                    like_total.style.display = 'none'
                }

                if (json.action_result === 'added') {
                    $('#like i[data-index="' + comment_id + '"]').addClass('fa-solid')
                } else {
                    $('#like i[data-index="' + comment_id + '"]').removeClass('fa-solid')
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })
});

function addReply(user, comment_id) {
    document.getElementById("contactparent").value = comment_id;
    const comment_form = document.getElementById("contactcomment")
    comment_form.innerText = `${user}, `;
    const end = comment_form.value.length;
    comment_form.setSelectionRange(end, end);
    comment_form.focus()
}