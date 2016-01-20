var index_page = function() {
    (function($){
        $('.activity-summary tr.agg-total > td > a').each(function () {
            var $this = $(this)
              , target = $this.data('target');
            
            $this.on('click', function () {
                $('[data-group="' + target + '"]').each(function () {
                    $(this).toggle();
                });
            });
        });
    })(jQuery);
}