<div class="panel panel-default">
    <div class="panel-heading">Import Stations on Feeder</div>
    <div class="panel-body">
        <form method="post">
            <table class="narrow-labels">
                <tbody>
                    <tr><td><label for="id_csv_file">CSV File: </label></td>
                        <td><input type="file" id="id_csv_file" name="csv_file" />
                </tbody>
            </table>
        </form>
    </div>
</div>
%rebase('admin/base.tpl', title=title, year=year)