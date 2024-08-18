box.cfg{
    listen = 3301
}

box.schema.user.create('admin', {password = 'presale', if_not_exists = true})
box.schema.user.grant('admin', 'read,write,execute', 'universe', nil, {if_not_exists = true})

box.schema.space.create('kv', {if_not_exists = true})
box.space.kv:format({
    {name = 'key', type = 'string'},
    {name = 'value', type = 'any'}
})
box.space.kv:create_index('primary', {parts = {'key'}, if_not_exists = true})