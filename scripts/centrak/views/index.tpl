% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
    <h1>Enumeration Captures</h1>
    <p>
        <a class="btn btn-primary" href="/activities">Sync Captures</a>
    </p>
</div>

<div class="row">
  <div class="heading" style="padding-left:20px;">{{ summary_type }}</div>
  <div class="col-md-8">
    <table class="table">
      <thead>
        <tr><th>Date</th><th>Total</th><th># Dup. RSeq</th>
            <th># Dup. Acct</th><th># New</th>
            <th>With Acct#</th><th># Active</th>
            <th># PPM</th></tr>
      </thead>
      <tbody>
      % if records:
        % for s in records:
        <tr><td>{{ s.date }}</td><td>{{ s.total }}</td>
            <td>{{ s.duplicated }}</td>
            <td>{{ s.dup_accts }}</td>
            <td>{{ s.new }}</td>
            <td>{{ s.accts }}</td><td>{{ s.active }}</td>
            <td>{{ s.ppms }}</td></tr>
        % end
      % else:
        <tr><td colspan="4">No data available</td></tr>
      % end 
      </tbody>
    </table>

    <div style="padding-top: 20px;">
        % for i in range(len(team_summary)):
        <div class="pull-left" style="width: 250px; border: solid 1px #ddd; padding:5px;">
        {{ team_summary.index[i] }}: &nbsp;&nbsp; <b>{{ team_summary[i] }}</b>
        </div>
        % end
        <div class="clearfix"></div>
    </div>

    <div style="padding-top: 20px;">
        % for i in range(len(ind_summary)):
        <div class="pull-left" style="width: 250px; border: solid 1px #ddd; padding:5px;">
        <b>{{ ind_summary.index[i].split('/')[0] }}</b> &nbsp;&nbsp;:&nbsp;&nbsp;{{ ind_summary.index[i].split('/')[1] }}:  
        <b class="pull-right">{{ ind_summary[i] }} &nbsp;&nbsp;</b>
        </div>
        % end
    </div>


  </div>
</div>