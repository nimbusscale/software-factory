# Functional spec

The functional spec for Facet: what the app should do, in the user's terms. Requirements are in
GEARS, with `FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

Facet is a self-hosted personal site for one person's résumé, portfolio and writing. Its main idea
is views: one set of content, shown differently to different audiences.

## F-SEC-1. Terms

- **Owner.** The one person who owns an instance and signs in to it.
- **Visitor.** Anyone who uses the site without signing in as the owner.
- **Instance.** One running copy of Facet, with its own data.
- **Site.** The pages of an instance that visitors see.
- **Admin.** The part of an instance where the owner signs in and changes the site.
- **Profile.** The owner's details shown on the site, such as their name, avatar, contact links and
  headline.
- **Item.** One piece of the owner's content, such as a job, a project, a talk or a post.
- **Fact field.** A field of an item that states a fact, such as a company name, a date, an
  institution or an issuer.
- **Framing field.** A field of an item that says how the item is described, such as its title,
  summary, description or bullets.
- **View.** A version of the site for one audience, such as recruiters, that chooses, orders and
  frames the owner's items (F-SEC-4).
- **View section.** A part of a view that shows a group of items.
- **View slug.** The short name that makes up a view's address, such as `recruiter` in
  `/recruiter`.
- **View visibility.** A view's setting for who can see it: public, unlisted, password or private
  (F-SEC-6). A view is named by this setting, such as an unlisted view or a password view.
- **Item visibility.** An item's setting for who can see it: public or private (F-SEC-6). An item
  is named by this setting, such as a public item or a private item.
- **Share link.** A link to an unlisted view that the owner gives out, of the form `/s/<token>`.
- **Homepage.** The page at the site's root address, `/`.
- **Site navigation.** The site's menu of links to its pages.
- **Import source.** An outside service the app copies the owner's content from, such as GitHub.
- **AI-assisted change.** A change to the owner's content that the app drafts with an AI model.
- **Proposal.** A set of changes from an import or an AI-assisted change, waiting for the owner to
  accept or reject them.
- **Analytics.** Figures about how visitors use the site, for the owner to look at.
- **Growth loop.** A feature that gets each visitor to bring in more people, such as a prompt to
  share the site or to invite others.

## F-SEC-2. Limits

**FR-1.** The app shall let only one person, the owner, sign in to an instance, with no other
users, roles, teams or tenants.

**FR-2.** The app shall hold only one profile per instance, not several.

*Why:* a family member who wants a site runs their own instance.

**FR-3.** The app shall run only as one container that exposes one port, not alongside other
services such as a database, a queue or a cache.

**FR-4.** The app shall keep all the instance's data, analytics included, only on the instance's
own disk, not in an outside service.

**FR-5.** The app shall keep only the current version of each item, not earlier versions.

*Why:* the owner's backups are the way back to an earlier version.

**FR-6.** The site shall have no engagement features, such as feeds, likes, follows or infinite
scroll.

*Why:* Facet is meant to be something a person runs for themselves, not a platform that runs
people.

**FR-7.** The site shall offer no private messages between visitors.

**FR-8.** The site shall show no advertising and no growth loops.

**FR-9.** The site shall include third-party tracking only where the owner has added it, not by
default.

**FR-10.** The app shall show the owner analytics only as information, not with goals or prompts
meant to change what the owner does.

**FR-11.** The app shall send email only to verify testimonials, to send notifications, and to
send newsletters the owner writes, not to carry messages between people.

**FR-12.** The app shall make content visible to more people only through a change the owner
makes, not as a side effect of anything else.

**FR-13.** The app shall apply changes from an import or an AI-assisted change only after the
owner accepts them, not on its own.

## F-SEC-3. The owner and the instance

**FR-14.** While the owner is signed in, the app shall let them see and change everything in the
instance.

**FR-15.** The app shall keep all of an instance's data in two folders, so that copying them backs
up the whole instance.

**FR-16.** When the owner asks for an export, the app shall give them a copy of all the instance's
data.

## F-SEC-4. Views

**FR-17.** The app shall let the owner show one item in any number of views.

*Why:* otherwise the owner would keep several copies of each item in step by hand.

**FR-18.** The app shall let the owner set each view section either to follow every public item
that fits it, or to show only the items the owner selects.

**FR-19.** While a view section is set to show selected items (FR-18) and none are selected, the
site shall show no items in that view section.

*Why:* falling back to every public item would publish items the owner didn't choose.

**FR-20.** When the owner opens or saves a view, the app shall keep each view section's setting
(FR-18) and selection as the owner left them.

**FR-21.** The app shall let the owner set the order a view shows its items in.

**FR-22.** The app shall let a view override only an item's framing fields, not its fact fields.

*Scenario:* Given a job, Product Designer at Acme Corp, shown in a view called UX Designer with
the title Senior UX Designer, and in a view called Instructional Designer with the title Learning
Experience Designer, when the owner changes the job's dates, then both views show the new dates,
each with its own title.

**FR-23.** The app shall let a view set its own headline, summary, hero image, call to action and
accent colour, but not its own name, avatar or contact links, which always come from the profile.

**FR-24.** The app shall let the owner add any view to the site navigation.

## F-SEC-5. Addresses

**FR-25.** The site shall build the homepage from the admin's homepage settings only, not from any
view.

**FR-26.** The site shall serve each view at its view slug right under the root address, such as
`/recruiter`, not under a prefix such as `/v/recruiter`.

*Why:* a short address reads better on a CV or a slide.

**FR-27.** When a visitor opens a view's address under `/v/`, such as `/v/recruiter`, the site
shall redirect them to the view's address, such as `/recruiter`.

*Why:* links to views with a `/v/` address are already in use elsewhere.

**FR-28.** When a visitor opens a valid share link, the site shall redirect them to the unlisted
view's address.

*Why:* this keeps the share link's token out of the browser's history, and stops it leaking to
other sites through the `Referer` header.

**FR-29.** When the owner sets a view slug, the app shall accept it only if none of Facet's own
pages uses that address.

## F-SEC-6. Who can see what

**FR-30.** Where a view is an unlisted view, the site shall show it only to a visitor who has
opened its share link.

**FR-31.** Where a view is a password view, the site shall show it only to a visitor who has
entered its password in the last hour.

*Accepted gap:* the owner can't end a visitor's access before the hour is up. This is accepted
because the access is short, and keeping no record of who has it keeps Facet simple.

**FR-32.** When a visitor opens a password view they can't yet see (FR-31), the site shall ask for
its password.

**FR-33.** Where a view or an item is private, the site shall show it only to the owner.

**FR-34.** When a visitor asks for an unlisted view without having opened its share link, or for a
private view or a private item, the site shall answer "not found".

*Why:* any other answer would confirm that it exists.

## F-SEC-7. Imports and AI-assisted changes

**FR-35.** The app shall let the owner accept or reject each field of a proposal on its own.

**FR-36.** The app shall let the owner lock any field they've edited by hand.

**FR-37.** When the app refreshes an item from its import source, the app shall propose no change
to the item's locked fields (FR-36).

**FR-38.** When the app drafts an AI-assisted change, the change shall add no facts or numbers
that aren't already in the owner's content.

**FR-39.** When the app drafts an AI-assisted change, the change shall be written in plain
language.

## F-SEC-8. Comments

**FR-40.** The site shall accept comments on an item only after the owner turns comments on for
that item.

**FR-41.** The app shall let the owner remove any comment.

## F-SEC-9. The admin

**FR-42.** While a part of the admin has nothing in it yet, the admin shall show guidance on
getting started there, not an error or a table of zeros.

## F-SEC-10. Accessibility and search

**FR-43.** The admin and the site shall each let the owner or a visitor reach and use every
control with the keyboard alone.

**FR-44.** The admin and the site shall each give every control a label that screen readers read
out.

**FR-45.** The site shall give each page its own title and description for search engines and link
previews.
