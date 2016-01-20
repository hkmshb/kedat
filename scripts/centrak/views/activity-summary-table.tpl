<div class="panel panel-default">
    <div class="panel-heading">
        <b>Captures Made Today</b>
    </div>
    <div class="panel-body">
        <table class="table panel-table table-figures">
            <thead>
                <tr class="group-desc">
                    <th></th><th></th><th></th>
                    <th colspan="2" class="lvsep col-shade">Duplicates</th>
                    <th colspan="4" class="lvsep">Account Status</th>
                    <th colspan="3" class="lvsep col-shade">Meter Type</th>
                </tr>
                <tr><th></th>
                    <th class="lvsep">Upriser</th>
                    <th class="lvsep">Total</th>
                    <th class="col-shade lvsep">#RS</th>
                    <th class="col-shade">#AC</th>

                    <th title="# New" class="lvsep">#.N</th>
                    <th title="# Active">#.A</th>
                    <th title="# Inactive">#.I</th>
                    <th title="# Unknown">#.U</th>

                    <th title="# Analogue" class="col-shade lvsep">#.Alog</th>
                    <th title="# PPM" class="col-shade">#.PPM</th>
                    <th title="# None" class="col-shade">#.NA</th>
                </tr>
            </thead>
            <tbody>
            % if records:
                % for r in records:
                <tr class="agg-total">
                    <td>{{ r.group }}</td>
                    <td class="lvsep text">-</td>
                    <td class="lvsep">{{ r._total }}</td>

                    <td class="col-shade lvsep">{{ r._rseq_duplicates }}</td>
                    <td class="col-shade">{{ r._acctno_duplicates }}</td>
                            
                    <td class="lvsep">{{ r.new }}</td>
                    <td>{{ r.active }}</td>
                    <td>{{ r.inactive }}</td>
                    <td>{{ r.unknown }}</td>

                    <td class="col-shade lvsep">{{ r.analogue }}</td>
                    <td class="col-shade">{{ r.ppm }}</td>
                    <td class="col-shade">{{ r.none }}</td>
                </tr>
                    % if r.uprisers:
 
                        % for u in r.uprisers:
                    <tr class="hide" data-group="{{ r.group }}">
                        <td>&nbsp;</td>
                        <td class="text">{{ u.upriser }}</td>
                        <td class="lvsep">{{ u._total }}</td>

                        <td class="col-shade lvsep">{{ u._rseq_duplicates }}</td>
                        <td class="col-shade">{{ u._acctno_duplicates }}</td>
                            
                        <td class="lvsep">{{ u.new }}</td>
                        <td>{{ u.active }}</td>
                        <td>{{ u.inactive }}</td>
                        <td>{{ u.unknown }}</td>

                        <td class="col-shade lvsep">{{ u.analogue }}</td>
                        <td class="col-shade">{{ u.ppm }}</td>
                        <td class="col-shade">{{ u.none }}</td>
                    </tr>
                        % end
                    % end
                % end
            % else:
                <tr><td colspan="8">No data available.</td></tr>
            % end
            </tbody>
        </table>
    </div>
</div>