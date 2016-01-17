% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
  <h1>Enumeration Captures</h1>
  <p>
    <a class="btn btn-primary" href="/activities">Sync Captures</a>
  </p>
</div>

<div class="row">
  <div class="heading" style="padding-left:20px;">Form Summaries</div>

  <div class="col-md-8">
    <table class="table">
      <thead>
        <tr><th>Form</th><th>Today</th><th>This Week</th><th>This Month</th><th>Total</th><tr>
      </thead>
      <tbody>
      % if records:
        % for r in records:
        <tr><td>{{ r.form }}</td>
            <td>{{ r.today }}</td>
            <td>{{ r.week }}</td>
            <td>{{ r.month }}</td>
            <td>{{ r.all }}</td></tr>
        % end
      % else:
        <tr><td colspan="">No data available</td></tr>
      % end
      </tbody>
    </table>
  </div>
</div>
