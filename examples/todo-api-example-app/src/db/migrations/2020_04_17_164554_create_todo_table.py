from orator.migrations import Migration


class CreateTodoTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('todo-items') as table:
            table.increments('id')
            table.string('text').nullable()
            table.boolean('done').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('todo-items')
