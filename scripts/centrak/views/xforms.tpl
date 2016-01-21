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
                            style="margin-top:-5px;">Get XForms (Sync)</button>
                </div>
            </div>
            <div class="panel-body">
                <table class="table panel-table">
                    <tbody>
                    % active_ids, all_ids = [], []
                    % if records:
                        % for r in records:
                        <tr><td><a href="/xforms/{{ r.id_string }}/">{{ r.title }}</a></td>
                            <td>{{ r.date_created }}</td>
                            <td><label for="activate-{{ r.id }}" class="table-label">
                                    <input type="checkbox" name="activate" value="{{ r.id_string }}"
                                           id="activate-{{ r.id }}" {{ "checked" if r.active else "" }} />
                                    Activate
                                </label>
                            </td></tr>
                            % all_ids.append(str(r.id_string))
                            % if r.active:
                                % active_ids.append(str(r.id_string)) 
                            % end
                        % end
                    % else:
                        <tr><td colspan="3">No data Available. Perform <b><i>Sync</i></b> to get XForms from server!</td></tr>
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
