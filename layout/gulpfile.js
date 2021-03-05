'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var rigger = require('gulp-rigger');

gulp.task('html', function(){
  gulp.src('src/*.html')
  .pipe(rigger())
  .pipe(gulp.dest('build/'));
});

gulp.task('sass', function () {
    gulp.src('src/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('../app/app/static/css/'));
});

gulp.task('icons', function() { 
    gulp.src('bower_components/fontawesome/fonts/**.*') 
    .pipe(gulp.dest('build/fonts')); 
});

gulp.task('js', function () {
    gulp.src('src/js/app.js')
    .pipe(rigger())
    .pipe(gulp.dest('../app/app/static/js/'));
});

gulp.task('build', [
    'sass',
    'html',
    'icons',
    'js'
]);

gulp.task('watch', function () {
  gulp.watch('src/sass/**/*.scss', ['sass']);
  gulp.watch('src/js/**/*.js', ['js']);
  gulp.watch('src/**/*.html', ['html']);
});

gulp.task('default', ['build', 'watch']);
