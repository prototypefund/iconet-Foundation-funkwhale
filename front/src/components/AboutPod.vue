<template>
  <main class="main pusher page-about" v-title="labels.title">
    <div class="ui container">
      <div class="ui horizontally fitted stripe basic segment">
        <div class="ui basic vertically fitted stripe segment content">
          <section :class="['ui', 'head', {'with-background': banner}, 'vertical', 'center', 'aligned', 'stripe', 'segment']" :style="headerStyle">
          </section>
        </div>
        <div class="ui basic vertically fitted stripe segment content">
          <!-- See layout in _about.scss -->
          <div class="about-pod-info-container">
            <!-- TODO: Table of contents -->
            <div class="about-pod-info-toc">
              <div class="ui vertical pointing secondary menu">
                <router-link to="/about/pod" class="item">
                  <translate translate-context="Content/About/Header">About this pod</translate>
                </router-link>
                <router-link to="/about/pod#rules" class="item">
                  <translate translate-context="Content/About/Header">Rules</translate>
                </router-link>
                <router-link to="/about/pod#terms" class="item">
                  <translate translate-context="Content/About/Header">Terms and privacy policy</translate>
                </router-link>
                <router-link to="/about/pod#features" class="item">
                  <translate translate-context="Content/About/Header">Features</translate>
                </router-link>
                <router-link v-if="stats" to="/about/pod#statistics" class="item">
                  <translate translate-context="Content/About/Header">Statistics</translate>
                </router-link>
              </div>
            </div>

            <div class="about-pod-info">
              <h2 class="ui header" id="description about-this-pod">
                <translate translate-context="Content/About/Header">About this pod</translate>
              </h2>
              <div v-html="markdown.makeHtml(longDescription)" v-if="longDescription"></div>
              <p v-else>
                <translate translate-context="Content/About/Paragraph">No description available.</translate>
              </p>

              <h3 class="ui header" id="rules">
                <translate translate-context="Content/About/Header">Rules</translate>
              </h3>
              <div v-html="markdown.makeHtml(rules)" v-if="rules"></div>
              <p v-else>
                <translate translate-context="Content/About/Paragraph">No rules available.</translate>
              </p>

              <h3 class="ui header" id="terms">
                <translate translate-context="Content/About/Header">Terms and privacy policy</translate>
              </h3>
              <div v-html="markdown.makeHtml(terms)" v-if="terms"></div>
              <p v-else>
                <translate translate-context="Content/About/Paragraph">No terms available.</translate>
              </p>

              <h3 class="header" id="features">
                <translate translate-context="Content/About/Header/Name">Features</translate>
              </h3>
              <div class="features-container ui two column stackable grid">
                <div class="column">
                  <table class="ui very basic table">
                    <tbody>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Funkwhale version</translate>
                        </td>
                        <td v-if="version" class="right aligned">
                          <span class="features-status ui text">
                            {{ version }}
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <translate translate-context="*/*/*">N/A</translate>
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Federation</translate>
                        </td>
                        <td v-if="federationEnabled" class="right aligned">
                          <span class="features-status ui text">
                            <i class="check icon"></i>
                            <translate translate-context="*/*/*/State of feature">Enabled</translate>
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <i class="x icon"></i>
                            <translate translate-context="*/*/*/State of feature">Disabled</translate>
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Allow-list</translate>
                        </td>
                        <td v-if="allowListEnabled" class="right aligned">
                          <span class="features-status ui text">
                            <i class="check icon"></i>
                            <translate translate-context="*/*/*/State of feature">Enabled</translate>
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <i class="x icon"></i>
                            <translate translate-context="*/*/*/State of feature">Disabled</translate>
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="column">
                  <table class="ui very basic table">
                    <tbody>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Anonymous access</translate>
                        </td>
                        <td v-if="anonymousCanListen" class="right aligned">
                          <span class="features-status ui text">
                            <i class="check icon"></i>
                            <translate translate-context="*/*/*/State of feature">Enabled</translate>
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <i class="x icon"></i>
                            <translate translate-context="*/*/*/State of feature">Disabled</translate>
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Registrations</translate>
                        </td>
                        <td v-if="openRegistrations" class="right aligned">
                          <span class="features-status ui text">
                            <i class="check icon"></i>
                            <translate translate-context="*/*/*/State of registrations">Open</translate>
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <i class="x icon"></i>
                            <translate translate-context="*/*/*/State of registrations">Closed</translate>
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <translate translate-context="*/*/*">Upload quota</translate>
                        </td>
                        <td v-if="defaultUploadQuota" class="right aligned">
                          <span class="features-status ui text">
                            {{ defaultUploadQuota * 1000 * 1000 | humanSize }}
                          </span>
                        </td>
                        <td v-else class="right aligned">
                          <span class="features-status ui text">
                            <translate translate-context="*/*/*">N/A</translate>
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <template v-if="stats">
                <h3 class="header" id="statistics">
                  <translate translate-context="Content/About/Header">Statistics</translate>
                </h3>
                <div class="statistics-container">
                  <div class="statistics-statistic" v-if="stats.hours">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ parseInt(stats.hours).toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="parseInt(stats.hours)" translate-plural="hours of music">hour of music</translate>
                    </span>
                  </div>
                  <div class="statistics-statistic" v-if="stats.artists">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ stats.artists.toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="stats.artists" translate-plural="artists">artist</translate>
                    </span>
                  </div>
                  <div class="statistics-statistic" v-if="stats.albums">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ stats.albums.toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="stats.albums" translate-plural="albums">album</translate>
                    </span>
                  </div>
                  <div class="statistics-statistic" v-if="stats.tracks">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ stats.tracks.toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="stats.tracks" translate-plural="tracks">track</translate>
                    </span>
                  </div>
                  <div class="statistics-statistic" v-if="stats.users">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ stats.users.toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="stats.users" translate-plural="active users">active user</translate>
                    </span>
                  </div>
                  <div class="statistics-statistic" v-if="stats.listenings">
                    <span class="statistics-figure ui text">
                      <span class="ui big text"><strong>{{ stats.listenings.toLocaleString($store.state.ui.momentLocale) }}</strong></span>
                      <br />
                      <translate translate-context="Content/About/*" :translate-n="stats.listenings" translate-plural="listenings">listening</translate>
                    </span>
                  </div>
                </div>
              </template>

              <template v-if="contactEmail">
                <h3 class="ui header" id="contact">
                  <translate translate-context="Content/About/Header">Contact</translate>
                </h3>
                <!-- TODO: Moderators -->
                <div class="ui"></div>
                <a v-if="contactEmail" :href="`mailto:${contactEmail}`">
                  <translate translate-context="Content/About/Email" :translate-params="{ email: contactEmail }">Send us an email: %{ contactEmail }</translate>
                </a>
              </template>

              <div class="ui hidden divider"></div>
              <div class="ui fluid horizontally fitted basic clearing segment container">
                <router-link to="/about" class="ui left floated basic secondary button">
                  <i class="icon arrow left"></i>
                  <translate translate-context="Content/About/Paragraph">Introduction</translate>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { mapState } from "vuex"
import _ from '@/lodash'
import showdown from 'showdown'

import SignupForm from "@/components/auth/SignupForm"

export default {
  components: {
    SignupForm,
  },
  data () {
    return {
      markdown: new showdown.Converter(),
      showAllowedDomains: false,
    }
  },
  computed: {

  ...mapState({
      nodeinfo: state => state.instance.nodeinfo,
    }),
    labels() {
      return {
        title: this.$pgettext('Head/About/Title', "About")
      }
    },
    podName() {
      return _.get(this.nodeinfo, 'metadata.nodeName') || "Funkwhale"
    },
    banner () {
      return _.get(this.nodeinfo, 'metadata.banner')
    },
    shortDescription () {
      return _.get(this.nodeinfo, 'metadata.shortDescription')
    },
    longDescription () {
      return _.get(this.nodeinfo, 'metadata.longDescription')
    },
    rules () {
      return _.get(this.nodeinfo, 'metadata.rules')
    },
    terms () {
      return _.get(this.nodeinfo, 'metadata.terms')
    },
    stats () {
      let data = {
        users: _.get(this.nodeinfo, 'usage.users.activeMonth', null),
        hours: _.get(this.nodeinfo, 'metadata.library.music.hours', null),
        artists: _.get(this.nodeinfo, 'metadata.library.artists.total', null),
        albums: _.get(this.nodeinfo, 'metadata.library.albums.total', null),
        tracks: _.get(this.nodeinfo, 'metadata.library.tracks.total', null),
        listenings: _.get(this.nodeinfo, 'metadata.usage.listenings.total', null),
      }
      if (data.users === null || data.artists === null) {
        return
      }
      return data
    },
    contactEmail () {
      return _.get(this.nodeinfo, 'metadata.contactEmail')
    },
    anonymousCanListen () {
      return _.get(this.nodeinfo, 'metadata.library.anonymousCanListen')
    },
    allowListEnabled () {
      return _.get(this.nodeinfo, 'metadata.allowList.enabled')
    },
    allowListDomains () {
      return _.get(this.nodeinfo, 'metadata.allowList.domains')
    },
    version () {
      return _.get(this.nodeinfo, 'software.version')
    },
    openRegistrations () {
      return _.get(this.nodeinfo, 'openRegistrations')
    },
    defaultUploadQuota () {
      return _.get(this.nodeinfo, 'metadata.defaultUploadQuota')
    },
    federationEnabled () {
      return _.get(this.nodeinfo, 'metadata.library.federationEnabled')
    },
    headerStyle() {
      if (!this.banner) {
        return ""
      }
      return (
        "background-image: url(" +
        this.$store.getters["instance/absoluteUrl"](this.banner) +
        ")"
      )
    },
  }
}
</script>