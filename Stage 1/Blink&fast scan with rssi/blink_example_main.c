#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "led_strip.h"
#include "sdkconfig.h"

static const char *TAG = "example";

#define BLINK_GPIO CONFIG_BLINK_GPIO

#ifdef CONFIG_BLINK_LED_STRIP

static led_strip_handle_t led_strip;

void set_led_color(uint8_t r, uint8_t g, uint8_t b) {
    led_strip_set_pixel(led_strip, 0, r, g, b);
    led_strip_refresh(led_strip);
}

static void configure_led(void) {
    ESP_LOGI(TAG, "Configuring LED strip for RSSI color display.");
    led_strip_config_t strip_config = {
        .strip_gpio_num = BLINK_GPIO,
        .max_leds = 1,
    };
#if CONFIG_BLINK_LED_STRIP_BACKEND_RMT
    led_strip_rmt_config_t rmt_config = {
        .resolution_hz = 10 * 1000 * 1000,
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
#elif CONFIG_BLINK_LED_STRIP_BACKEND_SPI
    led_strip_spi_config_t spi_config = {
        .spi_bus = SPI2_HOST,
        .flags.with_dma = true,
    };
    ESP_ERROR_CHECK(led_strip_new_spi_device(&strip_config, &spi_config, &led_strip));
#else
#error "unsupported LED strip backend"
#endif
    led_strip_clear(led_strip);
}

#elif CONFIG_BLINK_LED_GPIO

void set_led_color(uint8_t r, uint8_t g, uint8_t b) {
    gpio_set_level(BLINK_GPIO, r > 0 || g > 0 || b > 0 ? 1 : 0);
}

static void configure_led(void) {
    ESP_LOGI(TAG, "Configuring GPIO LED for RSSI color display.");
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);
}

#else
#error "unsupported LED type"
#endif


// פונקציה למיפוי ערך RSSI לצבע
void rssi_to_color(int rssi, uint8_t* r, uint8_t* g, uint8_t* b) {
    if (rssi > -50) {
        *r = 255;
        *g = 0;
        *b = 0;  // אדום לאות חזק מאוד
    } else if (rssi > -60) {
        *r = 255;
        *g = 69;
        *b = 0;  // כתום כהה
    } else if (rssi > -70) {
        *r = 255;
        *g = 165;
        *b = 0;  // כתום
    } else if (rssi > -80) {
        *r = 255;
        *g = 255;
        *b = 0;  // צהוב
    } else if (rssi > -85) {
        *r = 173;
        *g = 255;
        *b = 47;  // ירוק בהיר
    } else if (rssi > -90) {
        *r = 0;
        *g = 255;
        *b = 0;  // ירוק לאות חלש
    } else {
        *r = 0;
        *g = 0;
        *b = 255;  // כחול לאות חלש מאוד
    }
}


void MotionDetector(void *param) {
    uint8_t r, g, b;

    while (1) {
        wifi_ap_record_t ap;
        esp_err_t err = esp_wifi_sta_get_ap_info(&ap);
        if (err == ESP_OK) {
            int strength = ap.rssi;
                printf("Wi-Fi Signal Strength:%d dBm\n", strength);

            // מיפוי ה-RSSI לצבע
            rssi_to_color(strength, &r, &g, &b);
            
            // שינוי צבע ה-LED בהתאם ל-RSSI
            set_led_color(r, g, b);
        } else {
            printf("Failed to get Wi-Fi AP info: %d\n", err);
            
            // אם אין גישה למידע על ה-Wi-Fi, כיבוי ה-LED
            set_led_color(0, 0, 0);
        }

        vTaskDelay(pdMS_TO_TICKS(1000)); // השהיה של שניה בין הבדיקות
    }
}

// מנהל האירועים לחיבור לרשת
static void event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        esp_wifi_connect();
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ESP_LOGI(TAG, "Got IP");
        xTaskCreate(&MotionDetector, "MotionDetector", 4096, NULL, 5, NULL);
    }
}

// פונקציה לחיבור WiFi עם Fast Scan
static void fast_scan(void) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, NULL));

    esp_netif_t *sta_netif = esp_netif_create_default_wifi_sta();
    assert(sta_netif);

    wifi_config_t wifi_config = {
                .sta = {
            .ssid = "Redmi Note 10S",
            .password = "shay1234",
            .scan_method = WIFI_FAST_SCAN,
            .sort_method = WIFI_CONNECT_AP_BY_SIGNAL,
            .threshold.rssi = -127,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}

void app_main(void) {
    configure_led();

    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    
    fast_scan();
}
