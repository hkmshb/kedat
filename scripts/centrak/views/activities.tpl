% rebase('layout.tpl', title=title, year=year)

<div class="row">
  <div class="col-md-8" style="padding-top: 20px">
    <form method="post" class="form-inline">
      <div class="form-group">
        <input type="date" class="form-control col-md-6" name="sync_date" 
               placeholder="Enter Sync Date" required />
      </div>
      <div class="form-group">
        <select class="form-control" name="sync_table" 
                placeholder="Select Table to Sync" required>
          <option value=""> &#171; Select Table to Sync &#187; </option>
          <option value="f000_cf04_KN">F000-CF04 (Training Form)</option>
        </select>
      </div>
      <button type="submit" class="btn btn-default">Sync</button>
    </form>
    
    <div class="heading" style="padding-top:20px; margin-bottom: -20px">Synched Tasks</div>
    <table class="table" style="margin-top:20px;">
      <thead>                                  
        <tr><th>Sync For</th><th>Table</th><th># Records</th><th>Performed</th></tr>
      </thead>
      <tbody>
      % if activities:
        % for record in activities:
        <tr><td>{{ record.sync_date}}</td>
            <td>{{ record.sync_table }}</td>
            <td>{{ record.record_count }}</td>
            <td>{{ record.date_created }}</td></tr>
        %end
      % else:
        <tr><td colspan="4">No data available</td></tr>
      % end
      </tbody>
    </table>
  </div>
</div>