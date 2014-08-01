<html>
    <head>
        <title>Antix Print Server</title>
        <link rel="stylesheet" type="text/css" media="screen" href="/static/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" media="screen" href="/static/font-awesome.min.css">
        <link rel="stylesheet" type="text/css" media="screen" href="/static/backgrid.css">
        <link rel="stylesheet" type="text/css" media="screen" href="/static/backgrid-text-cell.css">
        <link rel="stylesheet" type="text/css" media="screen" href="/static/style.css">
        <script type="text/javascript" src="/static/jquery-1.10.2.js"></script>
        <script type="text/javascript" src="/static/underscore.js"></script>
        <script type="text/javascript" src="/static/bootstrap.js"></script>
        <script type="text/javascript" src="/static/backbone.js"></script>
        <script type="text/javascript" src="/static/backgrid.js"></script>
        <script type="text/javascript" src="/static/backgrid-text-cell.js"></script>
        <script type="text/javascript" src="/static/moment-with-langs.js"></script>
        <script type="text/javascript" src="/static/app.js"></script>
        <script type="text/javascript">
            window.secret = "{{api_key}}";
            $(function() {
                (new Printers()).render();
            });
        </script>
    </head>
    <body>


    <!-- Head Start -->
    <div class="head">
        <div class="container">
            <div class="row" style="text-align: center; margin-bottom: 30px;">

                <h1>
                   <span><a href="javascript:"><i class="fa fa-print orange"></i> Antix Print Server</a></span>
                </h1>
                <span>Version 1.01</span>

            </div>
        </div>
    </div>
    <!-- Menu Bar End -->


    <!-- Inner Page Heading -->
    <div class="col-sm-12 col-md-12 col-lg-12" id="options">

        <div class="row col-sm-12 clearfix">
            <div class="col-md-12">
                <div class="box">
                    <div class="box-header" data-original-title>
                        <h2><i class="fa fa-print"></i><span class="break"></span>Printers</h2>
                        <div class="box-icon">
                            <a href="javascript:" class="save" title="Save" data-rel="tooltip"><i class="fa fa-save"></i></a>
                        </div>
                    </div>
                    <div class="box-content">
                        <div id="printers"></div>
                    </div>
                </div>
            </div>
        </div>

    </div>




    <div class="footer" style="text-align: center; margin-top: 30px;">
        <div class="footer-inner">
            <div class="container">
                <a href="/upgrade/{{api_key}}">Upgrade Server</a>
                <div class="copy">
                    <p>&copy; Copyright <a href="#">Antix &trade;</a></p>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer End -->


    </body>
</html>