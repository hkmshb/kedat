% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
    <h1>Enumeration Captures</h1>
    <p class="lead">{{ summary_type }}</p>
</div>

<div class="row">
  <div class="col-md-8">
    <table class="table">
      <thead>
        <tr><th>Total</th><th># Duplicates</th><th># Billable</th><th># Revisits</th></tr>
      </thead>
      <tbody>
      % for summary in records:
        <tr></tr>
      % else:
        <tr><td colspan="4">No data available</td></tr>
      % end 
      </tbody>
    </table>
  </div>
</div>