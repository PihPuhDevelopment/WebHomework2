(function () {
    $('.q-vote').on('click', function (event) {
        event.preventDefault();
        var $this = $(this);
        var qid = $this.data('qid');
        var vote = $this.data('vote');
        console.log('qid: ' + qid + " vote: " + vote);

        $.ajax({
            url: '/vote/',
            method: 'POST',
            data: {
                'qid': qid,
                'vote': vote
            },
            dataType: 'json',
            success: function (data) {
                if (data['ok'] === 1) {
                    $('#rating' + qid).text(data['rating']);
                }
            }
        })
    })
})();