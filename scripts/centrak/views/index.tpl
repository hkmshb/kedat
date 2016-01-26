<div class="jumbotron">
    <h1 class="pull-left">Project: Eagle Eye</h1>
    % include('calendar-input.tpl')
    % if ref_date != report_ref_date:
    <div style="margin-top: 65px">
        % include('calendar.tpl', calendar_class="coral", ref_date=report_ref_date, weekdate_bounds=report_weekdate_bounds)
    </div>
    % end
</div>

<div class="row">
    <div class="col-md-12">
      <!-- forms summary -->
      <form method="post">
        <div class="panel panel-default">
            <div class="panel-heading">
                {{ title }}
            </div>
            <div class="panel-body">
                <table class="table panel-table">
                    <thead>
                        <tr>
                            <th>XForm</th>
                            <th title="Today" class="lvsep">Today</th>
                            <th title="Today Duplicate RSeq">#DRS</th>
                            <th title="Today Duplicate A/C#">#DAC</th>

                            <th title="This Week"  class="lvsep col-shade">Week</th>
                            <th title="Week Duplicate RSeq" class="col-shade">#DRS</th>
                            <th title="Week Duplicate A/C#" class="col-shade">#DAC</th>

                            <th title="This Month" class="lvsep">Month</th>
                            <th title="Month Duplicate RSeq">#DRS</th>
                            <th title="Month Duplicate A/C#">#DAC</th>

                            <th title="Total" class="lvsep col-shade">All</th>
                            <th title="All Duplicate RSeq" class="col-shade">#DRS</th>
                            <th title="All Duplicate A/C#" class="col-shade">#DAC</th>
                        </tr>
                    </thead>
                    <tbody>
                    % if records:
                        % for r in records:
                        <tr><td><a href="/xforms/{{r.id_string}}/">{{ r.title }}</a></td>
                            <td class="lvsep">{{ r.d_total or '-' }}</td>
                            <td>{{ r.d_rseq_duplicates or '-' }}</td>
                            <td>{{ r.d_acctno_duplicates or '-' }}</td>

                            <td class="lvsep col-shade">{{ r.w_total or '-' }}</td>
                            <td class="col-shade">{{ r.w_rseq_duplicates or '-' }}</td>
                            <td class="col-shade">{{ r.w_acctno_duplicates or '-' }}</td>
                            
                            <td class="lvsep">{{ r.m_total or '-' }}</td>
                            <td>{{ r.m_rseq_duplicates or '-' }}</td>
                            <td>{{ r.m_acctno_duplicates or '-' }}</td>
                            
                            <td class="lvsep col-shade">{{ r._total or '-' }}</td>
                            <td class="col-shade">{{ r._rseq_duplicates or '-' }}</td>
                            <td class="col-shade">{{ r._acctno_duplicates or '-' }}</td></tr>
                        % end
                    % else:
                        <tr><td colspan="13">No data available. Perform <b><i>Sync Captures</i></b> to get Captures from server!</td></tr>
                    % end
                    </tbody>
                </table>
            </div>
        </div>
      </form>                                      
    </div>
</div>

<div class="row">
  <div class="col-md-10">
    % include('activity-summary-table.tpl', records=activity_records, stat=activity_stats)
  </div>
    <div class="col-md-2">
        <div class="panel panel-info">
            <div class="panel-heading">Report</div>
            <div class="panel-body">
                <form method="post" class="form-inline report-form" action="/r/default/">
                    <div class="form-group">
                        <div class="input-group date pull-left" style="width: 120px;">
                            <input type="text" class="form-control" placeholder="dd/mm/yyyy"
                                   required="" disabled="" value="{{report_ref_date.strftime('%d/%m/%Y')}}">
                                <span class="input-group-addon btn" style="border-radius: 0 4px 4px 0;">
                                    <i class="glyphicon glyphicon-th"></i>
                                </span>
                            </input>
                        </div>
                    </div>
                    <input type="hidden" name="ref_date" value="{{ report_ref_date.strftime('%Y-%m-%d')}}" />
                    <input type="hidden" name="form_id" value="f130_cf06_KN" />
                    <button type="submit" class="btn btn-primary" style="margin-top:3px;">Generate Report</button>
                </form>
            </div>
        </div>
    </div>
</div>

% def scripts():
<script>
    (function($) {
        $(function(){
           index_page(); 
           
           $('.date-input').datepicker({
                    format: "dd/mm/yyyy", clearBtn: true,
                    autoclose: true, toggleActive: true,
                    todayHighlight: true,           
               }).on('changeDate', function(e) {
                    var entry = e.format('yyyymmdd')
                      , url = window.location.origin;
                    
                    if (entry !== "")
                        url = url + '/?refdate=' + entry;
                    window.open(url, target='_self');
               });
               
           $('.input-group.date').datepicker({
                format: "dd/mm/yyyy", clearBtn: true,
                autoclose: true, toggleActive: true,
                todayHighlight: true,
           }).on('changeDate', function(e) {
                var entry = e.format('yyyy-mm-dd');
                $('.report-form [name=ref_date]').val(entry);
           });
        });
    })(jQuery);
</script>
% end
% rebase('layout.tpl', title=title, year=year, extra_scripts=scripts)