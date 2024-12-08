package com.healthapp.clientmobile.services;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;

import com.healthapp.clientmobile.R;
import com.healthapp.clientmobile.sensors.SensorData;

import java.util.ArrayList;
import java.util.Date;


public class SensorService extends Service implements SensorEventListener {
    private static final String TAG = "AccelerometerService";
    private final ArrayList<SensorData> accelerometerDataList = new ArrayList<>();
    private SensorManager sensorManager;
    private Sensor sensor;
    private Handler handler;
    private Runnable runnable;

    private String userId;

    @Override
    public void onCreate() {
        super.onCreate();
//        calAidApp = (CalAidApp) getApplicationContext();
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "onStartCommand: Service started");
        accelerometerDataList.clear();
        if(intent != null){
            if(intent.getAction() == "startAccService"){
                        handler = new Handler();
                        runnable = new Runnable() {
                            @Override
                            public void run() {
                                Log.d("CALAIDAPP -Acc service", "acc");
                                sendDataToDB();
                                handler.postDelayed(this, 10000);
                            }
                        };
                        handler.postDelayed(runnable, 10000);
                    }
                sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

                sensor = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
                sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_NORMAL);


                final String CHANNELID = "Foreground Service ID";
                createNotificationChannel(CHANNELID);
                Notification.Builder notification = new Notification.Builder(this, CHANNELID)
                        .setContentText("Collecting accelerometer data...")
                        .setContentTitle("")
                        .setSmallIcon(R.drawable.icon_launcher);

                startForeground(1001, notification.build());
            }
            if(intent.getAction() == "stopAccService"){
                stopForeground(true);
                stopSelf();

        }

        return START_NOT_STICKY;
    }

    @Override
    public void onDestroy() {
        Log.d(TAG, "onDestroy: Service destroyed");
        super.onDestroy();
        sensorManager.unregisterListener(this);
        handler.removeCallbacks(runnable);
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        Log.d(TAG,+ sensorEvent.values[0] + " " + sensorEvent.values[1] + " " + sensorEvent.values[2]);
        SensorData data = new SensorData();
        data.setUserId(userId);
        data.setX(sensorEvent.values[0]);
        data.setY(sensorEvent.values[1]);
        data.setZ(sensorEvent.values[2]);
        data.setTimestamp(new Date(System.currentTimeMillis()));
        accelerometerDataList.add(data);
    }

    private void sendDataToDB() {
        if (accelerometerDataList.size() > 0) {
            final ArrayList<SensorData> dataToSend = new ArrayList<>(accelerometerDataList);
            accelerometerDataList.clear();
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    private void createNotificationChannel(String CHANNEL_ID) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "CalAidApp";
            String description = "Collecting accelerometer data";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

}