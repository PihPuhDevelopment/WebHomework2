(function () {
    $('.ans-vote').on('click', function (event) {
        event.preventDefault();
        var $this = $(this);
        var ansid = $this.data('ansid');
        var vote = $this.data('vote');
        console.log('ansid: ' + ansid + ', vote: ' + vote);

        $.ajax({
            url: '/vote-answer/',
            method: 'POST',
            data: {
                'ansid': ansid,
                'vote': vote
            },
            dataType: 'json',
            success: function (data) {
                if (data['ok'] === 1) {
                    $('#ansrating' + ansid).text(data['rating']);
                }
            }
        })
    });
})();