 % rebase('layout.tpl', title=title, year=year)

 <div class="row">
    <div class="col-md-9">
        <div class="panel panel-default">
            <div class="panel-heading">
                {{ title }}
            </div>
            <div class="panel-body">
                <table border="0" class="table panel-table table-figures">
                    <thead>
                        <tr class="group-desc">
                            <th></th><th ></th>
                            <th colspan="2" class="lvsep col-shade">Duplicates</th>
                            <th colspan="4" class="lvsep">Account Status</th>
                            <th colspan="3" class="lvsep col-shade">Meter Type</th>
                        </tr>
                        <tr><th>&nbsp;</th>
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
                        <tr><td>{{ r.date }}</td>
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
                        % end
                    % else:
                        <tr><td>No data available.</td></tr>
                    % end
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <div class="col-md-3">
        % include('calendar.tpl')
    </div>
 </div>