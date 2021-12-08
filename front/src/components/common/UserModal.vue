<template>
  <!-- TODO make generic and move to semantic/modal? -->
  <modal
    :show="show"
    :scrolling="true"
    :fullscreen="false"
    @update:show="$emit('update:show', $event)"
  >
    <div
      v-if="$store.state.auth.authenticated"
      class="header"
    >
      <img
        v-if="$store.state.auth.profile.avatar && $store.state.auth.profile.avatar.urls.medium_square_crop"
        v-lazy="$store.getters['instance/absoluteUrl']($store.state.auth.profile.avatar.urls.medium_square_crop)"
        alt=""
        class="ui centered small circular image"
      >
      <actor-avatar
        v-else
        :actor="{preferred_username: $store.state.auth.username, full_username: $store.state.auth.username,}"
      />
      <h3 class="user-modal title">
        {{ labels.header }}
      </h3>
    </div>
    <div
      v-else
      class="header"
    >
      <h3 class="ui center aligned icon header">
        {{ labels.header }}
      </h3>
    </div>
    <div class="content">
      <div class="ui one column unstackable grid">
        <div class="row">
          <div
            class="column"
            role="button"
            @click="[$emit('update:show', false), $emit('showLanguageModalEvent')]"
          >
            <i class="language icon user-modal list-icon" />
            <span class="user-modal list-item">{{ labels.language }}:</span>
            <div class="right floated">
              <span class="user-modal list-item">{{ $language.available[$language.current] }}</span>
              <i class="action-hint chevron right icon" />
            </div>
          </div>
        </div>
        <div class="row">
          <div
            class="column"
            role="button"
            @click="[$emit('update:show', false), $emit('showThemeModalEvent')]"
          >
            <i class="palette icon user-modal list-icon" />
            <span class="user-modal list-item">{{ labels.theme }}:</span>
            <div class="right floated">
              <span class="user-modal list-item"> {{ themes.find(x => x.key ===$store.state.ui.theme).name }}</span>
              <i class="action-hint chevron right icon user-modal" />
            </div>
          </div>
        </div>
        <div class="ui divider" />
        <template v-if="$store.state.auth.authenticated">
          <div class="row">
            <div
              class="column"
              role="button"
              @click.prevent.exact="$router.push({name: 'profile.overview', params: { username: $store.state.auth.username }})"
            >
              <i class="user icon user-modal list-icon" />
              <span class="user-modal list-item">{{ labels.profile }}</span>
            </div>
          </div>
          <div class="row">
            <router-link
              v-if="$store.state.auth.authenticated"
              tag="div"
              class="column"
              :to="{name: 'notifications'}"
              role="button"
            >
              <i class="user-modal list-icon bell icon" />
              <span class="user-modal list-item">{{ labels.notifications }}</span>
            </router-link>
          </div>
          <div class="row">
            <router-link
              tag="div"
              class="column"
              :to="{ path: '/settings' }"
              role="button"
            >
              <i class="user-modal list-icon cog icon" />
              <span class="user-modal list-item">{{ labels.settings }}</span>
            </router-link>
          </div>
          <div class="ui divider" />
        </template>
        <div class="row">
          <a
            class="column"
            href="https://funkwhale.audio/help"
            target="_blank"
          >
            <i class="user-modal list-icon life ring outline icon" />
            <span class="user-modal list-item">{{ labels.help }}</span>
          </a>
        </div>
        <div class="row">
          <a
            class="column"
            href="https://docs.funkwhale.audio"
            target="_blank"
          >
            <i class="user-modal list-icon book open icon" />
            <span class="user-modal list-item">{{ labels.docs }}</span>
          </a>
        </div>
        <div class="row">
          <router-link
            tag="div"
            class="column"
            :to="{ name: 'about' }"
            role="button"
          >
            <i class="user-modal list-icon question circle outline icon" />
            <span class="user-modal list-item">{{ labels.about }}</span>
          </router-link>
        </div>
        <div class="ui divider" />
        <template v-if="$store.state.auth.authenticated">
          <router-link
            tag="div"
            class="column"
            :to="{ name: 'logout' }"
            role="button"
          >
            <i class="user-modal list-icon sign out alternate icon" />
            <span class="user-modal list-item">{{ labels.logout }}</span>
          </router-link>
        </template>
        <template v-if="!$store.state.auth.authenticated">
          <router-link
            tag="div"
            class="column"
            :to="{ name: 'login' }"
            role="button"
          >
            <i class="user-modal list-icon sign in alternate icon" />
            <span class="user-modal list-item">{{ labels.login }}</span>
          </router-link>
        </template>
        <template
          v-if="!$store.state.auth.authenticated"
          &&
          $store.state.instance.settings.users.registration_enabled.value
        >
          <router-link
            tag="div"
            class="column"
            :to="{ name: 'signup' }"
            role="button"
          >
            <i class="user-modal list-item user icon" />
            <span class="user-modal list-item">{{ labels.signup }}</span>
          </router-link>
        </template>
      </div>
    </div>
  </modal>
</template>

<script>
import Modal from '@/components/semantic/Modal'
import { mapGetters } from 'vuex'

export default {
  components: {
    Modal
  },
  props: {
    show: { type: Boolean, required: true }
  },
  computed: {
    labels () {
      return {
        header: this.$pgettext('Popup/Title/Noun', 'Options'),
        profile: this.$pgettext('*/*/*/Noun', 'Profile'),
        settings: this.$pgettext('*/*/*/Noun', 'Settings'),
        logout: this.$pgettext('Sidebar/Login/List item.Link/Verb', 'Log out'),
        about: this.$pgettext('Sidebar/About/List item.Link', 'About'),
        shortcuts: this.$pgettext('*/*/*/Noun', 'Keyboard shortcuts'),
        support: this.$pgettext('Sidebar/*/Listitem.Link', 'Help'),
        forum: this.$pgettext('Sidebar/*/Listitem.Link', 'Forum'),
        docs: this.$pgettext('Sidebar/*/Listitem.Link', 'Documentation'),
        help: this.$pgettext('Sidebar/*/Listitem.Link', 'Help'),
        language: this.$pgettext(
          'Sidebar/Settings/Dropdown.Label/Short, Verb',
          'Language'
        ),
        theme: this.$pgettext(
          'Sidebar/Settings/Dropdown.Label/Short, Verb',
          'Theme'
        ),
        chat: this.$pgettext('Sidebar/*/Listitem.Link', 'Chat room'),
        git: this.$pgettext('Sidebar/*/List item.Link', 'Issue tracker'),
        login: this.$pgettext('*/*/Button.Label/Verb', 'Log in'),
        signup: this.$pgettext('*/*/Button.Label/Verb', 'Sign up'),
        notifications: this.$pgettext('*/Notifications/*', 'Notifications'),
        useOtherInstance: this.$pgettext(
          'Sidebar/*/List item.Link',
          'Use another instance'
        )
      }
    },
    themes () {
      return [
        {
          icon: 'sun icon',
          name: this.$pgettext(
            'Footer/Settings/Dropdown.Label/Theme name',
            'Light'
          ),
          key: 'light'
        },
        {
          icon: 'moon icon',
          name: this.$pgettext(
            'Footer/Settings/Dropdown.Label/Theme name',
            'Dark'
          ),
          key: 'dark'
        }
      ]
    },
    ...mapGetters({
      additionalNotifications: 'ui/additionalNotifications'
    })
  }
}
</script>

<style>
.action-hint {
  margin-left: 1rem !important;
}
</style>