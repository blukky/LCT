package io.indrian16.customtab.about;

import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;
import android.view.MenuItem;

import io.indrian16.customtab.R;
import com.xgc1986.parallaxPagerTransformer.ParallaxPagerTransformer;

D:\zxz\zx\CustomTab-master\app\src\main\java\io\indrian16\customtab\about\MainActivity.java
public class MainActivity extends FragmentActivity {

    ViewPager mPager;
    DemoParallaxAdapter mAdapter;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.demo_activity_parallax);

        mPager = (ViewPager) findViewById(R.id.pager);
       // mPager.setBackgroundColor(0xFF000000);

        ParallaxPagerTransformer pt = new ParallaxPagerTransformer((R.id.image));
      //  pt.setBorder(20);
        //pt.setSpeed(0.2f);
        mPager.setPageTransformer(false, pt);

        mAdapter = new DemoParallaxAdapter(getSupportFragmentManager());
        mAdapter.setPager(mPager); //only for this transformer

        Bundle bNina = new Bundle();
        bNina.putInt("image", R.drawable.m5);
        bNina.putString("name", "Данные об уровене загрязнения в районе");
        DemoParallaxFragment pfNina = new DemoParallaxFragment();
        pfNina.setArguments(bNina);

        Bundle bNiju = new Bundle();
        bNiju.putInt("image", R.drawable.m7);
        bNiju.putString("name", "Определение уровеня экологии");
        DemoParallaxFragment pfNiju = new DemoParallaxFragment();
        pfNiju.setArguments(bNiju);

        Bundle bYuki = new Bundle();
        bYuki.putInt("image", R.drawable.m3);
        bYuki.putString("name", "Прогнозирование благоприятных для жизни районов");
        DemoParallaxFragment pfYuki = new DemoParallaxFragment();
        pfYuki.setArguments(bYuki);



          Bundle bKero1 = new Bundle();
        bKero1.putInt("image", R.drawable.m9);
        bKero1.putString("name", "Статистика загрязнения воздуха");
        DemoParallaxFragment bfKero1 = new DemoParallaxFragment();
        bfKero1.setArguments(bKero1);

          Bundle bKero2 = new Bundle();
        bKero2.putInt("image", R.drawable.m10);
        bKero2.putString("name", "Kero");
        DemoParallaxFragment bfKero2 = new DemoParallaxFragment();
        bfKero2.setArguments(bKero2);


        mAdapter.add(pfNina);
        mAdapter.add(pfNiju);
        mAdapter.add(pfYuki);
      //  mAdapter.add(pfKero);
        mAdapter.add(bfKero1);
     //   mAdapter.add(bfKero2);
        mPager.setAdapter(mAdapter);

        if (getActionBar() != null) {
            getActionBar().setDisplayHomeAsUpEnabled(true);
            getActionBar().show();
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        onBackPressed();

        return super.onOptionsItemSelected(item);
    }
}
