var handleThemePanelExpand = function() {
    $(document).on('click', '[data-click="filter-panel-expand"]', function () {
        var e = '.filter-panel',
        a = 'active';
        $(e).hasClass(a) ? $(e).removeClass(a) : $(e).addClass(a)
    })
},
handleActivitySummaryRowToggle = function() {
    $('.activity-summary tr.agg-total > td > a').each(function () {
        var $this = $(this)
          , target = $this.data('target');

        $this.on('click', function () {
            $('[data-group="' + target + '"]').each(function () {
                $(this).toggle();
            });
        });
    });
},
handleCaptureFiltering = function() {
    var query = "", entry = ""
      , fnames = ['datetime_today', 'enum_id', 'rseq', 'acct_status', 'acct_no',
                  'meter_status', 'meter_type', 'sort_by', 'then_by']
    for (fn in fnames) {
        entry = $('[name=' + fnames[fn] + ']').val();
        if (entry !== undefined && entry !== "") {
            query += (fnames[fn] + "=" + entry + "&");
        }

        var pathname = window.location.pathname;
        window.location = pathname + '?' + encodeURI(query);
    }
    return false;
};

App = function () {
    'use strict';
    return {
        init: function () {
            // init all select2
            $('.select2').select2();

            handleActivitySummaryRowToggle(),
            handleThemePanelExpand()
        },
        filterCapture: function() { 
            $('[name=filter]').on('click', function () {
                return handleCaptureFiltering();
            });
        },
    }
}();


(function ($) {
    App.init();
})(jQuery);
