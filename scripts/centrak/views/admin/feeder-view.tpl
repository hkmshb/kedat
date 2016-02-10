<table class="table table-condensed">
    <tbody>
        <tr style="border-bottom:solid 1px #ddd;">
            <td style="white-space:nowrap; width:100px;">
                <label class="control-label">Feeder: </lable>
            </td>
            <td style="width:100px;">{{ feeder.code }}</td>
            <td style="width:80%;">{{ feeder.voltage }}KV {{ feeder.name }}</td>
            <td><a href="{{ '/admin/feeders/%s/edit' % feeder.code.lower() }}">
                    <i class="glyphicon glyphicon-edit"></i>
                </a>
            </td>
        </tr>
    </tbody>
</table>
<div class="panel panel-default">
    <div class="panel-heading">
        <b>Stations</b>
        <div class="pull-right">
            <div style="margin-top: -5px;">
                <a href="{{ '/admin/feeders/%s/station/create' % feeder.code.lower() }}" class="btn btn-default">Add</a>
                <a href="{{ '/admin/feeders/%s/station/import' % feeder.code.lower() }}" class="btn btn-default">Import</a>
                <button type="submit" name="del" class="btn btn-danger">Delete</button>
            </div>
        </div>
    </div>
    <div class="panel-body">
        <table class="table table-condensed table-hover">
            <thead>
                <tr><th>Code</th><th>Name</th><th>Rating</th></tr>
            </thead>
            <tbody>
            % if stations:
                % for s in stations:
                <tr><td><a href="{{ '/admin/feeders/%s/station/%s/' % (feeder.code.lower(), s.code.lower()) }}">{{ s.code }}</a></td>
                    <td>{{ s.name }}</td>
                    <td>{{ s.capacity }}KVA, {{ get_vratio_display(s.vratio) or ''}}</td></tr>
                % end
            % else:
                <tr><td colspan="4">No data available.</td></tr>
            % end
            </tbody>
        </table>
    </div>
</div>
%rebase('admin/base.tpl', title=title, year=year)