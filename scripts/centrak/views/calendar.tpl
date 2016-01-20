<div class="calendar pull-right">
    <div class="pull-left">
        <i class="glyphicon glyphicon-calendar"></i>
    </div>
    <div class="pull-right body">
        <span class="tdy">{{ ref_date.strftime('%A, %B %d, %Y') }}</span>
        <br/>
        <span class="wk">
            {{ weekdate_bounds[0].strftime('%b %d, %Y') }} - 
            {{ weekdate_bounds[1].strftime('%b %d, %Y') }}
        </span>
    </div>
</div>