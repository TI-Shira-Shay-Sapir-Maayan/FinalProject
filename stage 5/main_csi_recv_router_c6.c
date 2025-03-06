/* Get recv router csi

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"

#include "nvs_flash.h"

#include "esp_mac.h"
#include "rom/ets_sys.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_now.h"

#include "lwip/inet.h"
#include "lwip/netdb.h"
#include "lwip/sockets.h"
#include "ping/ping_sock.h"

#include "protocol_examples_common.h"

#define CONFIG_SEND_FREQUENCY      100
#define MACSTR "%02x:%02x:%02x:%02x:%02x:%02x"


static const char *TAG = "csi_recv_router";

static void wifi_csi_rx_cb(void *ctx, wifi_csi_info_t *info)
{
    if (!info || !info->buf) {
        ESP_LOGW(TAG, "<%s> wifi_csi_cb", esp_err_to_name(ESP_ERR_INVALID_ARG));
        return;
    }

    if (memcmp(info->mac, ctx, 6)) {
        return;
    }

    static int s_count = 0;
    const wifi_pkt_rx_ctrl_t *rx_ctrl = &info->rx_ctrl;

    if (!s_count) {
        ESP_LOGI(TAG, "================ CSI RECV ================");
        ets_printf("type,seq,mac,rssi,rate,sig_mode,mcs,bandwidth,smoothing,not_sounding,aggregation,stbc,fec_coding,sgi,noise_floor,ampdu_cnt,channel,secondary_channel,local_timestamp,ant,sig_len,rx_state,len,first_word,data\n");
    }

    /** Only LLTF sub-carriers are selected. */
    info->len = 128;

 printf("CSI_DATA- " MACSTR ", %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %lu, %d, %d, %d, %d, %d, %d, %d", 
    MAC2STR(info->mac), 
    s_count++, rx_ctrl->rssi, rx_ctrl->rate, rx_ctrl->timestamp, rx_ctrl->sig_len,
    rx_ctrl->rx_state, rx_ctrl->channel, rx_ctrl->channel, rx_ctrl->cur_bb_format,
    rx_ctrl->cur_single_mpdu, rx_ctrl->noise_floor, rx_ctrl->rxend_state,
    rx_ctrl->second, rx_ctrl->rx_channel_estimate_info_vld, rx_ctrl->rx_channel_estimate_len,
    rx_ctrl->he_siga1, rx_ctrl->he_siga2, rx_ctrl->he_sigb_len, rx_ctrl->is_group,
    rx_ctrl->rxmatch0, rx_ctrl->rxmatch1, rx_ctrl->rxmatch2, rx_ctrl->rxmatch3);

    // MACSTR ",%d, "     MAC2STR(info->mac)

    printf(",%d,%d,\"[%d", info->len, info->first_word_invalid, info->buf[0]);

    for (int i = 1; i < info->len; i++) {
        printf(",%d", info->buf[i]);
    }

    printf("]\"\n");
    }

static void wifi_csi_init()
{
    /**
     * @brief In order to ensure the compatibility of routers, only LLTF sub-carriers are selected.
     */
  wifi_csi_acquire_config_t csi_config = {
    .enable = 1,                          /**< enable to acquire CSI */
    .acquire_csi_legacy = 1,              /**< enable to acquire L-LTF */
    .acquire_csi_ht20 = 1,                /**< enable to acquire HT-LTF when receiving an HT20 PPDU */
    .acquire_csi_ht40 = 1,                /**< enable to acquire HT-LTF when receiving an HT40 PPDU */
    .acquire_csi_su = 1,                  /**< enable to acquire HE-LTF when receiving an HE20 SU PPDU */
    .acquire_csi_mu = 1,                  /**< enable to acquire HE-LTF when receiving an HE20 MU PPDU */
    .acquire_csi_dcm = 1,                 /**< enable to acquire HE-LTF when receiving an HE20 DCM applied PPDU */
    .acquire_csi_beamformed = 1,          /**< enable to acquire HE-LTF when receiving an HE20 Beamformed applied PPDU */
    .val_scale_cfg = 8,                   /**< value 0-8 */
    .dump_ack_en = 0,                     /**< enable to dump 802.11 ACK frame, default disabled */
    .reserved = 0,                        /**< reserved field */
};



    static wifi_ap_record_t s_ap_info = {0};
    ESP_ERROR_CHECK(esp_wifi_sta_get_ap_info(&s_ap_info));
    ESP_ERROR_CHECK(esp_wifi_set_csi_config(&csi_config));
    ESP_ERROR_CHECK(esp_wifi_set_csi_rx_cb(wifi_csi_rx_cb, s_ap_info.bssid));
    ESP_ERROR_CHECK(esp_wifi_set_csi(true));
}

static esp_err_t wifi_ping_router_start()
{
    static esp_ping_handle_t ping_handle = NULL;

    esp_ping_config_t ping_config = ESP_PING_DEFAULT_CONFIG();
    ping_config.count             = 0;
    ping_config.interval_ms       = 1000 / CONFIG_SEND_FREQUENCY;
    ping_config.task_stack_size   = 3072;
    ping_config.data_size         = 1;

    esp_netif_ip_info_t local_ip;
    esp_netif_get_ip_info(esp_netif_get_handle_from_ifkey("WIFI_STA_DEF"), &local_ip);
    ESP_LOGI(TAG, "got ip:" IPSTR ", gw: " IPSTR, IP2STR(&local_ip.ip), IP2STR(&local_ip.gw));
    ping_config.target_addr.u_addr.ip4.addr = ip4_addr_get_u32(&local_ip.gw);
    ping_config.target_addr.type = ESP_IPADDR_TYPE_V4;

    esp_ping_callbacks_t cbs = { 0 };
    esp_ping_new_session(&ping_config, &cbs, &ping_handle);
    esp_ping_start(ping_handle);

    return ESP_OK;
}

void app_main()
{
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    /**
     * @brief This helper function configures Wi-Fi, as selected in menuconfig.
     *        Read "Establishing Wi-Fi Connection" section in esp-idf/examples/protocols/README.md
     *        for more information about this function.
     */
    ESP_ERROR_CHECK(example_connect());

    wifi_csi_init();
    wifi_ping_router_start();
}