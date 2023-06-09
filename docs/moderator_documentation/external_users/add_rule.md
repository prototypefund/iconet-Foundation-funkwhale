# Add a moderation rule

```{warning}
Purging a user's data removes all objects and caches associated to that user. This impacts users who have objects from these users in their libraries.
```

Add moderation rules to users to control how they can interact with your {term}`pod`. Moderation rules enable you to restrict content from a user showing on your pod.

:::{dropdown} Required permissions
:icon: key

- {guilabel}`Moderation` – provides access to the administration and moderation menus.

:::

To add a moderation rule to a user:

::::{tab-set}

:::{tab-item} Desktop
:sync: desktop

1. Log in to your {term}`pod`.
2. Select the wrench icon ({fa}`wrench`) at the top of the sidebar to open the {guilabel}`Administration` menu.
3. Select {guilabel}`Moderation`. The {guilabel}`Reports` page opens.
4. Select {guilabel}`Accounts` at the top of the page. The {guilabel}`Accounts` page opens. You can see a list of known accounts on this page.
5. Select the account you want to apply the rule to. The account's moderation page opens.
6. Select {guilabel}`Add a moderation policy`. The moderation policy form appears.
7. Enter the {guilabel}`Reason` you are applying the rule. Depending on your pod's configuration, users may be able to see this.
8. Choose your moderation rule:
   - {guilabel}`Block everything` – purge all content from the user and block all content.
   - {guilabel}`Reject media` – only reject media files such as audio files, avatars, and album art.
9. Select {guilabel}`Create` to save your rule.

:::

:::{tab-item} Mobile
:sync: mobile

1. Log in to your {term}`pod`.
2. Select the wrench icon ({fa}`wrench`) at the top of the screen to open the {guilabel}`Administration` menu.
3. Select {guilabel}`Moderation`. The {guilabel}`Reports` page opens.
4. Select {guilabel}`Accounts` at the top of the page. The {guilabel}`Accounts` page opens. You can see a list of known accounts on this page.
5. Select the account you want to apply the rule to. The account's moderation page opens.
6. Select {guilabel}`Add a moderation policy`. The moderation policy form appears.
7. Enter the {guilabel}`Reason` you are applying the rule. Depending on your pod's configuration, users may be able to see this.
8. Choose your moderation rule:
   - {guilabel}`Block everything` – purge all content from the user and block all content.
   - {guilabel}`Reject media` – only reject media files such as audio files, avatars, and album art.
9. Select {guilabel}`Create` to save your rule.

:::
::::

That's all there is to it! You've applied your moderation rule. The rule takes effect as soon as you create it.
