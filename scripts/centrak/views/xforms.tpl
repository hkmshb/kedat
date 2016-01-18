% rebase('layout.tpl', title=title, year=year)

<div class="row">
    <div class="col-md-8">
      <form method="post">
        <div class="panel panel-default">
            <div class="panel-heading">
                XForms
                <div class="pull-right">
                    <button type="submit" name="save" class="btn btn-success"
                            style="margin-top:-5px;">Save</button>
                    <button type="submit" name="sync" class="btn btn-primary" 
                            style="margin-top:-5px;">Sync</button>
                </div>
            </div>
            <div class="panel-body">
                <table class="table panel-table">
                    <tbody>
                    % if records:
                        % active_ids, all_ids = [], []
                        % for r in records:
                        <tr><td>{{ r.title }}</td>
                            <td>{{ r.date_created }}</td>
                            <td><label for="activate-{{ r.id }}" class="table-label">
                                    <input type="checkbox" name="activate" value="{{ r.id }}"
                                           id="activate-{{ r.id }}" {{ "checked" if r.active else "" }} />
                                    Activate
                                </label>
                            </td></tr>
                            % all_ids.append(str(r.id))
                            % if r.active:
                                % active_ids.append(str(r.id)) 
                            % end
                        % end
                    % else:
                        <tr><td colspan="3">Empty!</td></tr>
                    % end
                    </tbody>
                </table>
                <input type="hidden" name="startup-all" value="{{ ','.join(all_ids) }}" />
                <input type="hidden" name="startup-active" value="{{ ','.join(active_ids) }}" />
            </div>
        </div>
      </form>
       

    </div>
</div>
