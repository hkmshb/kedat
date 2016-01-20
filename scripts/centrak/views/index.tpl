% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
    <h1>Project: Eagle Eye</h1>
    <p>
        <a class="btn btn-primary" href="#">Sync Captures</a>
    </p>
    <div class="pull-right calendar">
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
                        <tr><th>XForm</th>
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
                            <th title="All Duplicate A/C#" class="col-shade">#DAC</th></tr>
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
    % include('activity-summary-table.tpl', records=activity_records)
  </div>
</div>