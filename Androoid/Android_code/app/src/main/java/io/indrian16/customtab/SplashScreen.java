package io.indrian16.customtab;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.WindowManager;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;


public class SplashScreen extends AppCompatActivity {

    private boolean isFirstAnimation = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash_screen);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS, WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS);


        /*Simple hold animation to hold ImageView in the centre of the screen at a slightly larger
        scale than the ImageView's original one.*/
        final Animation hold = AnimationUtils.loadAnimation(this, R.anim.hold);
        Animation poyavlenir = AnimationUtils.loadAnimation(this, R.anim.poyavlenir);
        Animation translate_scale_shift_left = AnimationUtils.loadAnimation(this, R.anim.translate_scale_shift_left);

        /* Translates ImageView from current position to its original position, scales it from
        larger scale to its original scale.*/
        final Animation translateScale = AnimationUtils.loadAnimation(this, R.anim.translate_scale);
        final Animation slide_out_left = AnimationUtils.loadAnimation(this, R.anim.slide_out_left);

        final ImageView imageView = findViewById(R.id.header_icon);

        final ImageView text_logo_app  = findViewById(R.id.text_logo_app);
        final TextView header_text  = findViewById(R.id.header_text);
        text_logo_app.setVisibility(View.GONE);
        header_text.setVisibility(View.GONE);

        translateScale.setAnimationListener(new Animation.AnimationListener() {
            @Override
            public void onAnimationStart(Animation animation) {

            }

            @Override
            public void onAnimationEnd(Animation animation) {
                if (!isFirstAnimation) {
                    imageView.clearAnimation();
                    Intent intent = new Intent( SplashScreen.this, io.indrian16.customtab.about.MainActivity.class);
                    startActivity(intent);
                    finish();
                }

                isFirstAnimation = true;
            }

            @Override
            public void onAnimationRepeat(Animation animation) {

            }
        });

        slide_out_left.setAnimationListener(new Animation.AnimationListener() {
            @Override
            public void onAnimationStart(Animation animation) {

            }

            @Override
            public void onAnimationEnd(Animation animation) {
                Intent intent = new Intent( SplashScreen.this, io.indrian16.customtab.about.MainActivity.class);
                startActivity(intent);

                finish();
            }

            @Override
            public void onAnimationRepeat(Animation animation) {

            }
        });
        hold.setAnimationListener(new Animation.AnimationListener() {
            @Override
            public void onAnimationStart(Animation animation) {

            }

            @Override
            public void onAnimationEnd(Animation animation) {
              //  header_text.setAnimation(slide_out_left);
              //  header_text.setVisibility(View.VISIBLE);
            }

            @Override
            public void onAnimationRepeat(Animation animation) {

            }
        });

        poyavlenir.setAnimationListener(new Animation.AnimationListener() {
            @Override
            public void onAnimationStart(Animation animation) {

            }

            @Override
            public void onAnimationEnd(Animation animation) {
                text_logo_app.startAnimation(hold);
                text_logo_app.setVisibility(View.VISIBLE);

                header_text.setAnimation(slide_out_left);
                header_text.setVisibility(View.VISIBLE);

            }

            @Override
            public void onAnimationRepeat(Animation animation) {

            }
        });
        imageView.startAnimation(poyavlenir);


    }
}
