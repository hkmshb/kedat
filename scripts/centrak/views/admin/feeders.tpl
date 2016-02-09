<form method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            <b>Feeders</b>
            <div class="pull-right">
                <div style="margin-top: -5px;">
                    <a href="/admin/feeders/create" class="btn btn-default">Add</a>
                    <button type="submit" name="del" class="btn btn-danger">Delete</button>
                </div>
            </div>
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th>Code</th><th>Voltage</th><th>Name</th></tr>
                </thead>
                <tbody>
                % if records:
                    % for r in records:
                    <tr><td style="white-space:nowrap;"><a href="/admin/feeders/{{ r.code.lower() }}/">{{ r.code }}</a></td>
                        <td>{{ r.voltage }}KV</td>
                        <td>{{ r.name }}</td>
                    </tr>
                    % end
                % else:
                    <tr><td colspan="2">No data available.</td></tr>
                % end
                </tbody>
            </table>
        </div>
    </div>
</form>
% rebase('admin/base.tpl', title=title, year=year)