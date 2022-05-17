def index_page(self, givenPort, givenIP):
    return """<!DOCTYPE html>
    <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
    <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
    <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
    <!--[if gt IE 8]>      <html class="no-js"> <!--<![endif]-->
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title></title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="">
        </head>
        <body>
            <!--[if lt IE 7]>
                <p class="browsehappy">You are using an <strong>outdated</strong> browser. Please <a href="#">upgrade your browser</a> to improve your experience.</p>
            <![endif]-->
            <h1>Welcome!</h1>
    
            <h2>Sign In</h2>
            <p>Log in to your account.</p>
            <hr>
            
            <form action="http://{ipAddress}:{port}/signIn" method="post">
                <label for="email"><b>Email</b></label>
                <input type="text" placeholder="Enter Email" name="email" required>
    
                <label for="psw"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="psw" required>
    
                <button type="submit">Sign In</button>
            </form>
    
            <p>If you don't have an account, consider to sign up.</p>
    
            <h2>Sign Up</h2>
            <p>Please fill in this form to create an account.</p>
            <hr>
            
            <form action="http://{ipAddress}:{port}/signUp" method="post">
                <label for="email"><b>Email</b></label>
                <input type="text" placeholder="Enter Email" name="email" required>
    
                <label for="psw"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="psw" required>
    
                <button type="submit">Sign Up</button>
            </form>
            <a href="http://{ipAddress}:{port}/traccia.pdf" download="traccia.pdf" >Scarica Traccia</a>
            <script src="" async defer></script>
        </body>
    </html>""".format(port=givenPort, ipAddress=givenIP)