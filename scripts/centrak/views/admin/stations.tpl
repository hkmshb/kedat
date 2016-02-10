<form method="post">
    <div class="panel panel-default">
        <div class="panel-heading">
            <b>{{ title }}</b>
            % if station_type != 'D':
            <div class="pull-right">
                <div style="margin-top: -5px;">
                    <a href="/admin/stations/create" class="btn btn-default">Add</a>
                    <button type="submit" name="del" class="btn btn-danger">Delete</button>
                </div>
            </div>
            % end
        </div>
        <div class="panel-body">
            <table class="table panel-table">
                <thead>
                    <tr><th style="width:150px;">Code</th>
                        <th style="width:400px;">Name</th>
                        <th style="width:300px;">Rating</th>
                        <th style="width:30%">Source Feeder</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                % if records:
                    % for r in records:
                    <tr><td style="white-space:nowrap;"><a href="/admin/stations/{{ r.code.lower() }}/">{{ r.code }}</a></td>
                        <td>{{ r.name }}</td>
                        <td>{{ r.capacity }}KVA, {{ get_vratio_display(r.vratio) }}</td>
                        % fdr = get_feeder(r.source_feeder)
                        <td>{{ fdr.voltage }}KV {{ fdr.name }}</td>
                        <td>
                            <a href="{{ '/admin/stations/%s/edit' % r.code.lower() }}">
                                <i class="glyphicon glyphicon-edit"></i>
                            </a>
                        </td>
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