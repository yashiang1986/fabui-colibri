<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInitc069c47a864f912d50ef02c26a76cc19
{
    public static $files = array (
        'ad155f8f1cf0d418fe49e248db8c661b' => __DIR__ . '/..' . '/react/promise/src/functions_include.php',
        '0e6d7bf4a5811bfa5cf40c5ccd6fae6a' => __DIR__ . '/..' . '/symfony/polyfill-mbstring/bootstrap.php',
    );

    public static $prefixLengthsPsr4 = array (
        'Z' => 
        array (
            'Zend\\Validator\\' => 15,
            'Zend\\Uri\\' => 9,
            'Zend\\Stdlib\\' => 12,
            'Zend\\Loader\\' => 12,
            'Zend\\Http\\' => 10,
            'Zend\\Escaper\\' => 13,
        ),
        'S' => 
        array (
            'Symfony\\Polyfill\\Mbstring\\' => 26,
            'Symfony\\Component\\Routing\\' => 26,
            'Symfony\\Component\\HttpFoundation\\' => 33,
            'Symfony\\Component\\EventDispatcher\\' => 34,
        ),
        'R' => 
        array (
            'React\\Stream\\' => 13,
            'React\\Socket\\' => 13,
            'React\\Promise\\' => 14,
            'React\\EventLoop\\' => 16,
            'Ratchet\\' => 8,
        ),
        'M' => 
        array (
            'MatthiasMullie\\PathConverter\\' => 29,
            'MatthiasMullie\\Minify\\' => 22,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'Zend\\Validator\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-validator/src',
        ),
        'Zend\\Uri\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-uri/src',
        ),
        'Zend\\Stdlib\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-stdlib/src',
        ),
        'Zend\\Loader\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-loader/src',
        ),
        'Zend\\Http\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-http/src',
        ),
        'Zend\\Escaper\\' => 
        array (
            0 => __DIR__ . '/..' . '/zendframework/zend-escaper/src',
        ),
        'Symfony\\Polyfill\\Mbstring\\' => 
        array (
            0 => __DIR__ . '/..' . '/symfony/polyfill-mbstring',
        ),
        'Symfony\\Component\\Routing\\' => 
        array (
            0 => __DIR__ . '/..' . '/symfony/routing',
        ),
        'Symfony\\Component\\HttpFoundation\\' => 
        array (
            0 => __DIR__ . '/..' . '/symfony/http-foundation',
        ),
        'Symfony\\Component\\EventDispatcher\\' => 
        array (
            0 => __DIR__ . '/..' . '/symfony/event-dispatcher',
        ),
        'React\\Stream\\' => 
        array (
            0 => __DIR__ . '/..' . '/react/stream/src',
        ),
        'React\\Socket\\' => 
        array (
            0 => __DIR__ . '/..' . '/react/socket/src',
        ),
        'React\\Promise\\' => 
        array (
            0 => __DIR__ . '/..' . '/react/promise/src',
        ),
        'React\\EventLoop\\' => 
        array (
            0 => __DIR__ . '/..' . '/react/event-loop/src',
        ),
        'Ratchet\\' => 
        array (
            0 => __DIR__ . '/..' . '/cboden/ratchet/src/Ratchet',
        ),
        'MatthiasMullie\\PathConverter\\' => 
        array (
            0 => __DIR__ . '/..' . '/matthiasmullie/path-converter/src',
        ),
        'MatthiasMullie\\Minify\\' => 
        array (
            0 => __DIR__ . '/..' . '/matthiasmullie/minify/src',
        ),
    );

    public static $prefixesPsr0 = array (
        'S' => 
        array (
            'SimpleJsonRpcClient\\' => 
            array (
                0 => __DIR__ . '/..' . '/jalle19/simple-json-rpc-client/src',
            ),
        ),
        'J' => 
        array (
            'JsonRPC' => 
            array (
                0 => __DIR__ . '/..' . '/fguillot/json-rpc/src',
            ),
        ),
        'G' => 
        array (
            'Guzzle\\Stream' => 
            array (
                0 => __DIR__ . '/..' . '/guzzle/stream',
            ),
            'Guzzle\\Parser' => 
            array (
                0 => __DIR__ . '/..' . '/guzzle/parser',
            ),
            'Guzzle\\Http' => 
            array (
                0 => __DIR__ . '/..' . '/guzzle/http',
            ),
            'Guzzle\\Common' => 
            array (
                0 => __DIR__ . '/..' . '/guzzle/common',
            ),
        ),
        'E' => 
        array (
            'Evenement' => 
            array (
                0 => __DIR__ . '/..' . '/evenement/evenement/src',
            ),
        ),
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInitc069c47a864f912d50ef02c26a76cc19::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInitc069c47a864f912d50ef02c26a76cc19::$prefixDirsPsr4;
            $loader->prefixesPsr0 = ComposerStaticInitc069c47a864f912d50ef02c26a76cc19::$prefixesPsr0;

        }, null, ClassLoader::class);
    }
}
