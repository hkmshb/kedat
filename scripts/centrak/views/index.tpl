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
        <tr><th>Date</th><th>Total</th><th># Duplicates</th><th># Billable</th><th># Revisits</th></tr>
      </thead>
      <tbody>
      % if records:
        % for summary in records:
        <tr></tr>
        % end
      % else:
        <tr><td colspan="4">No data available</td></tr>
      % end 
      </tbody>
    </table>
  </div>
</div>